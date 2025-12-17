# BASIC USAGE INFORMATION
#
# The script is designed to be run from IDA as a script (File -> Script Command).
# The function used for decryption is selected based on the current cursor position.
# !! The script assumes that the boundaries of the given function are correctly defined !!
# (the emulation is terminated if an emulated instruction lies outside these boundaries)
# --------------------------------------------------------------------------------------------------------

import idaapi
import idc
import ida_funcs
import ida_bytes
import idautils
import ida_ida
import ida_ua
import ida_segment
import ida_nalt
import time
from unicorn import *
from unicorn.x86_const import *

# --------------------------------------------------------------------------------------------------------
# CONFIGURATION
MAX_INSTRUCTIONS_TOTAL = 10000000
MAX_PATHS = 10000
STACK_BASE = 0x00100000
STACK_SIZE = 0x00200000
REG_BLOCK_SIZE = 1 * 1024 * 1024
HEAP_BASE = 0x60000000
# --------------------------------------------------------------------------------------------------------

class IdaUnicornEmulator:
    def __init__(self):
        self.uc = None
        self.is_64bit = ida_ida.inf_is_64bit()
        self.arch = UC_ARCH_X86
        self.mode = UC_MODE_64 if self.is_64bit else UC_MODE_32

        if self.is_64bit:
            self.reg_ip = UC_X86_REG_RIP
            self.reg_sp = UC_X86_REG_RSP
        else:
            self.reg_ip = UC_X86_REG_EIP
            self.reg_sp = UC_X86_REG_ESP

        self.mapped_pages = set()
        self.stop_request = False

        self.tick_count = 0
        self.last_movaps_tick = -100
        self.xmm_buffer = bytearray()
        self.first_movaps_addr = 0

        self.path_queue = []
        self.visited_branches = set()
        self.results = {}

        self.current_path_id = 0
        self.total_paths_spawned = 0

    def set_hexrays_comment(self, address, text):
        try:
            cfunc = idaapi.decompile(address)
            if cfunc:
                tl = idaapi.treeloc_t()
                tl.ea = address
                tl.itp = idaapi.ITP_SEMI
                cfunc.set_user_cmt(tl, text)
                cfunc.save_user_cmts()
        except:
            pass

    def set_comment(self, address, text):
        current = idc.get_cmt(address, 0) or ""
        if text not in current:
            idc.set_cmt(address, f"{current} | {text}" if current else text, 0)
        self.set_hexrays_comment(address, text)

    def _align_page(self, addr):
        return addr & ~(0xFFF)

    def _align_size(self, size):
        return (size + 0xFFF) & ~(0xFFF)

    def flush_xmm_buffer(self):
        if not self.xmm_buffer:
            return
        raw_data = self.xmm_buffer.rstrip(b"\x00")
        if not raw_data:
            self.xmm_buffer = bytearray()
            self.first_movaps_addr = 0
            return

        hex_str = raw_data.hex()
        ascii_text, wide_text = "", ""
        ascii_score, wide_score = 0.0, 0.0

        try:
            ascii_text = "".join(chr(b) if 32 <= b < 127 else "." for b in raw_data)
            valid_ascii = sum(1 for b in raw_data if 32 <= b < 127)
            ascii_score = valid_ascii / len(raw_data) if len(raw_data) > 0 else 0
        except:
            pass

        try:
            raw_wide = raw_data
            if len(raw_wide) % 2 != 0:
                raw_wide += b"\x00"
            decoded_wide = raw_wide.decode("utf-16le")
            printable_wide = sum(1 for c in decoded_wide if c.isprintable())
            wide_score = (
                printable_wide / len(decoded_wide) if len(decoded_wide) > 0 else 0
            )
            wide_text = decoded_wide.replace("\x00", "")
        except:
            pass

        cmt_text = ""
        priority = 3
        if ascii_score > 0.85:
            priority = 1
            cmt_text = f'Decrypted: "{ascii_text}"'
        elif wide_score > 0.85:
            priority = 2
            cmt_text = f'Decrypted: L"{wide_text}"'
        else:
            priority = 3
            cmt_text = (
                f"Decrypted HEX: {hex_str[:32]}{'...' if len(hex_str)>32 else ''}"
            )

        addr = self.first_movaps_addr
        if addr not in self.results or priority < self.results[addr][0]:
            self.results[addr] = (priority, cmt_text)
            self.set_comment(addr, cmt_text)

        self.xmm_buffer = bytearray()
        self.first_movaps_addr = 0

    def setup_unicorn(self):
        self.uc = Uc(self.arch, self.mode)
        self.uc.mem_map(STACK_BASE, STACK_SIZE)
        stack_top = STACK_BASE + (STACK_SIZE // 2)
        self.uc.reg_write(self.reg_sp, stack_top)

        if self.is_64bit:
            regs = [
                UC_X86_REG_RAX,
                UC_X86_REG_RBX,
                UC_X86_REG_RCX,
                UC_X86_REG_RDX,
                UC_X86_REG_RSI,
                UC_X86_REG_RDI,
                UC_X86_REG_R8,
                UC_X86_REG_R9,
                UC_X86_REG_R10,
                UC_X86_REG_R11,
                UC_X86_REG_R12,
                UC_X86_REG_R13,
                UC_X86_REG_R14,
                UC_X86_REG_R15,
            ]
        else:
            regs = [
                UC_X86_REG_EAX,
                UC_X86_REG_EBX,
                UC_X86_REG_ECX,
                UC_X86_REG_EDX,
                UC_X86_REG_ESI,
                UC_X86_REG_EDI,
            ]

        total_heap = self._align_size(len(regs) * REG_BLOCK_SIZE)
        self.uc.mem_map(HEAP_BASE, total_heap)
        self.uc.mem_write(HEAP_BASE, b"\x00" * total_heap)

        for i, reg in enumerate(regs):
            self.uc.reg_write(reg, HEAP_BASE + (i * REG_BLOCK_SIZE))

        for seg_ea in idautils.Segments():
            seg = ida_segment.getseg(seg_ea)
            if not seg:
                continue
            aligned_start = self._align_page(seg.start_ea)
            aligned_end = self._align_size(seg.end_ea - aligned_start + aligned_start)
            size = aligned_end - aligned_start
            if size == 0 or aligned_start in self.mapped_pages:
                continue
            try:
                self.uc.mem_map(aligned_start, size, UC_PROT_ALL)
                data = ida_bytes.get_bytes(aligned_start, size)
                if data:
                    self.uc.mem_write(aligned_start, data)
                self.mapped_pages.add(aligned_start)
            except:
                pass

    def hook_mem_unmapped(self, uc, access, address, size, value, user_data):
        page_addr = self._align_page(address)
        try:
            uc.mem_map(page_addr, 0x1000)
            db_data = ida_bytes.get_bytes(page_addr, 0x1000)
            if db_data:
                uc.mem_write(page_addr, db_data)
            else:
                uc.mem_write(page_addr, b"\x00" * 0x1000)
            return True
        except:
            return False

    def hook_code(self, uc, address, size, user_data):
        self.tick_count += 1
        if self.tick_count >= MAX_INSTRUCTIONS_TOTAL:
            self.stop_request = True
            uc.emu_stop()
            return

        insn = idautils.DecodeInstruction(address)
        if not insn:
            return

        mnem = idc.print_insn_mnem(address).lower()
        op1 = idc.print_operand(address, 0)
        op2 = idc.print_operand(address, 1)

        if insn.itype in [idaapi.NN_retn, idaapi.NN_retf]:
            uc.emu_stop()
            return

        # --------------------------------------------------------------------------------------------------------
        # STRING EXTRACTION
        #
        # The decrypted string is stored in memory using the instruction:
        #        movaps  xmmword ptr [mem], xmm0
        if mnem == "movaps" and op2.lower() == "xmm0":
            val_int = uc.reg_read(UC_X86_REG_XMM0)
            chunk = val_int.to_bytes(16, byteorder="little")
            if self.tick_count - self.last_movaps_tick > 10:
                self.flush_xmm_buffer()
                self.first_movaps_addr = address
            self.xmm_buffer.extend(chunk)
            self.last_movaps_tick = self.tick_count

        # --------------------------------------------------------------------------------------------------------
        # SWITCH FORK
        #
        # Fork the execution for all possible switch targets
        if mnem.startswith("jmp") and insn.Op1.type != idaapi.o_near:
            sw_info = ida_nalt.switch_info_t()
            is_switch = ida_nalt.get_switch_info(sw_info, address)
            if is_switch or True:
                targets = list(idautils.CodeRefsFrom(address, 1))
                if len(targets) > 1:
                    ctx = uc.context_save()
                    try:
                        stack = uc.mem_read(STACK_BASE, STACK_SIZE)
                    except:
                        stack = b""

                    added = 0
                    for target in targets:
                        # Max Paths Check
                        if len(self.path_queue) >= MAX_PATHS:
                            break

                        branch_id = (address, target)
                        if branch_id not in self.visited_branches:
                            self.visited_branches.add(branch_id)
                            self.total_paths_spawned += 1
                            self.path_queue.append(
                                (target, ctx, stack, self.total_paths_spawned)
                            )
                            added += 1

                    if added > 0:
                        self.stop_request = True
                        uc.emu_stop()
                        return

        # --------------------------------------------------------------------------------------------------------
        # LOOP KILLER (prevent backward jumps)
        target_addr_loop = None

        # A) Direct Jump
        if mnem.startswith("j") and insn.Op1.type in [idaapi.o_near, idaapi.o_far]:
            target_addr_loop = insn.Op1.addr
        # B) Indirect (Register)
        elif mnem.startswith("j") and insn.Op1.type == idaapi.o_reg:
            reg_map = {
                "eax": UC_X86_REG_EAX,
                "ebx": UC_X86_REG_EBX,
                "ecx": UC_X86_REG_ECX,
                "edx": UC_X86_REG_EDX,
                "esi": UC_X86_REG_ESI,
                "edi": UC_X86_REG_EDI,
                "ebp": UC_X86_REG_EBP,
                "esp": UC_X86_REG_ESP,
            }
            if op1.lower() in reg_map:
                target_addr_loop = uc.reg_read(reg_map[op1.lower()])

        # If backward jump -> skip it (force continue)
        if target_addr_loop is not None and target_addr_loop < address:
            next_addr = address + size
            uc.reg_write(self.reg_ip, next_addr)
            self.stop_request = True
            uc.emu_stop()
            return  # Don't process forks for this instruction, we killed it.

        # --------------------------------------------------------------------------------------------------------
        # JUMP FORKING
        #
        # If encounter a jmp instruction, fork the execution for all of its cross-references
        # Combined with some control-flow deobfuscation, this allows for more accurate results
        if mnem.startswith("jmp"):
            ida_targets = list(idautils.CodeRefsFrom(address, 1))
            if len(ida_targets) > 0:
                ctx = uc.context_save()
                stack = uc.mem_read(STACK_BASE, STACK_SIZE)

                for t in ida_targets:
                    # Ignore backward jumps even in IDA hints if we want to kill loops
                    if t < address:
                        continue

                    branch_id = (address, t)
                    if (
                        branch_id not in self.visited_branches
                        and len(self.path_queue) < MAX_PATHS
                    ):
                        self.visited_branches.add(branch_id)
                        self.total_paths_spawned += 1
                        self.path_queue.append(
                            (t, ctx, stack, self.total_paths_spawned)
                        )

        # --------------------------------------------------------------------------------------------------------
        # CONDITIONAL FORK
        #
        # For the execution for conditional jumps
        is_cond = insn.itype >= idaapi.NN_ja and insn.itype <= idaapi.NN_jz
        if is_cond and len(self.path_queue) < MAX_PATHS:
            target = insn.Op1.addr
            # If conditional jump is backward, do not fork (to prevent loops)
            if target > address:
                fallthrough = address + size
                branch_id = (address, target)
                if branch_id not in self.visited_branches:
                    self.visited_branches.add(branch_id)
                    self.total_paths_spawned += 1
                    ctx = uc.context_save()
                    try:
                        stack = uc.mem_read(STACK_BASE, STACK_SIZE)
                    except:
                        stack = b""
                    self.path_queue.append(
                        (target, ctx, stack, self.total_paths_spawned)
                    )
                    uc.reg_write(self.reg_ip, fallthrough)

        # --------------------------------------------------------------------------------------------------------
        # CALL HANDLING
        #
        # When skipping function calls, it is crucial to correctly align the stack. Otherwise, the decryption
        # would produce meaningless data. Therefore, individual calling conventions must be properly handled.
        if insn.itype in [idaapi.NN_call, idaapi.NN_callfi, idaapi.NN_callni]:
            next_addr = address + size
            is_cdecl = False
            sp_adj = 0

            # Try to find "ADD ESP, X" after the call (Standard CDECL)
            try:
                next_i = idautils.DecodeInstruction(next_addr)
                if (
                    next_i
                    and next_i.itype == idaapi.NN_add
                    and next_i.Op1.type == idaapi.o_reg
                    and next_i.Op1.reg == 4
                ):

                    if next_i.Op2.type == idaapi.o_imm:
                        is_cdecl = True
                        sp_adj = next_i.Op2.value
                        next_addr += (
                            next_i.size
                        )
            except:
                pass

            if not is_cdecl:
                # Heuristic: Backwards Scan (Strict PUSH only)
                scan_ptr = address
                stack_adjustment = 0
                word_size = 8 if self.is_64bit else 4

                MAX_INSTRUCTIONS_SCAN = 60
                for _ in range(MAX_INSTRUCTIONS_SCAN):
                    scan_ptr = idc.prev_head(scan_ptr)
                    if scan_ptr == idaapi.BADADDR:
                        break

                    pi = idautils.DecodeInstruction(scan_ptr)
                    if not pi:
                        break

                    # If encounter a control flow instruction, stop
                    if pi.itype in [
                        idaapi.NN_call,
                        idaapi.NN_callfi,
                        idaapi.NN_callni,
                        idaapi.NN_retn,
                        idaapi.NN_retf,
                        idaapi.NN_jmp,
                        idaapi.NN_jmpfi,
                        idaapi.NN_jmpni,
                        idaapi.NN_jb,
                        idaapi.NN_jbe,
                        idaapi.NN_jae,
                        idaapi.NN_ja,
                        idaapi.NN_jl,
                        idaapi.NN_jle,
                        idaapi.NN_jge,
                        idaapi.NN_jg,
                        idaapi.NN_js,
                        idaapi.NN_jns,
                        idaapi.NN_jo,
                        idaapi.NN_jno,
                        idaapi.NN_jp,
                        idaapi.NN_jnp,
                        idaapi.NN_jz,
                        idaapi.NN_jnz,
                    ]:
                        break

                    # Classic PUSH - counting
                    if pi.itype == idaapi.NN_push:
                        stack_adjustment += word_size

                    # SUB/ADD ESP -> stop (prolog or other block)
                    elif (
                        (pi.itype == idaapi.NN_sub or pi.itype == idaapi.NN_add)
                        and pi.Op1.type == idaapi.o_reg
                        and pi.Op1.reg == 4
                    ):  # 4 = ESP
                        break

                    # Check basic block boundary (Xref)
                    if any(idautils.CodeRefsTo(scan_ptr, 0)):
                        break

                if stack_adjustment > 0:
                    sp_adj = stack_adjustment

                # Heuristic: SUB ESP allocation (GCC/Clang style)
                # Runs only if we found neither pushes nor CDECL cleanup
                if sp_adj == 0:
                    current_func = ida_funcs.get_func(address)
                    func_start = current_func.start_ea if current_func else 0

                    scan_ptr = address
                    for _ in range(60):
                        scan_ptr = idc.prev_head(scan_ptr)
                        if scan_ptr == idaapi.BADADDR:
                            break
                        pi = idautils.DecodeInstruction(scan_ptr)
                        if not pi:
                            break

                        # Looking for: sub esp, imm
                        if (
                            pi.itype == idaapi.NN_sub
                            and pi.Op1.type == idaapi.o_reg
                            and pi.Op1.reg == 4              # ESP = 4
                            and pi.Op2.type == idaapi.o_imm
                        ):
                            # If 'sub esp' is too close to function start (< 64 bytes),
                            # consider it a prolog and ignore it.
                            dist_from_start = scan_ptr - func_start
                            if (
                                func_start > 0
                                and dist_from_start >= 0
                                and dist_from_start < 0x40
                            ):
                                break
                            sp_adj = pi.Op2.value
                            break

                        # Stop at flow boundaries
                        if pi.itype in [idaapi.NN_retn, idaapi.NN_jmp, idaapi.NN_call]:
                            break

            # Applying stack adjustment
            if sp_adj > 0:
                esp = uc.reg_read(self.reg_sp)
                uc.reg_write(self.reg_sp, esp + sp_adj)

            uc.reg_write(self.reg_ip, next_addr)
            self.stop_request = True
            uc.emu_stop()

    def run_one_path(self, start_addr, end_ea):
        self.uc.reg_write(self.reg_ip, start_addr)
        curr = start_addr

        while True:
            flags = ida_bytes.get_flags(curr)
            if not ida_bytes.is_code(flags) or not ida_bytes.is_head(flags):
                break
            if curr >= end_ea:
                break

            try:
                self.stop_request = False
                self.uc.emu_start(curr, end_ea, count=0, timeout=0)

                if self.stop_request:
                    if self.tick_count >= MAX_INSTRUCTIONS_TOTAL:
                        return
                    curr = self.uc.reg_read(self.reg_ip)
                    continue
                else:
                    break
            except UcError as e:
                break
            except Exception as e:
                break

        self.flush_xmm_buffer()

    def get_name_or_hex(self, ea):
        func = ida_funcs.get_func(ea)
        if func and func.start_ea == ea:
            name = ida_funcs.get_func_name(ea)
            return f"<{name}>"

        return hex(ea)

    def run(self, ea):
        func = ida_funcs.get_func(ea)
        if not func:
            print("Error: Cursor not in func.")
            return

        print(f"[Starting Branching Extraction]: {self.get_name_or_hex(func.start_ea)}")
        self.setup_unicorn()
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.hook_mem_unmapped)
        self.uc.hook_add(UC_HOOK_CODE, self.hook_code)
        self.current_path_id = 0
        self.run_one_path(func.start_ea, func.end_ea)

        while self.path_queue and self.tick_count < MAX_INSTRUCTIONS_TOTAL:
            target, ctx, stack, pid = self.path_queue.pop(0)
            self.current_path_id = pid

            try:
                self.uc.context_restore(ctx)
                self.uc.mem_write(STACK_BASE, bytes(stack))
                self.run_one_path(target, func.end_ea)
            except Exception as e:
                print(f"Restore failed: {e}")

        print("-" * 60)
        for addr in sorted(self.results.keys()):
            prio, text = self.results[addr]
            print(f"[0x{addr:X}] {text}")
        print("-" * 60)
        print(f"Finished. Paths: {self.total_paths_spawned+1}, Instructions: {self.tick_count}")


if __name__ == "__main__":
    total_start = time.time()
    emu = IdaUnicornEmulator()
    emu.run(idc.here())
    total_end = time.time()
    print(f"Total processing time: {total_end - total_start:.2f} seconds")