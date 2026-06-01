# MIT License
#
# Copyright (c) 2026 Gen Digital Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Vidar string decryptor (emulation-based, IDA + Unicorn).

Tested with:
    296C97D66AC4CB05777F053FA2C17E78B415567E449D169AA3CF683A6565D28A (Vidar version 1.5)
    16911BD74F0D6751A30A1BE56A3752DAF7BF333C0D6EC61D8746646DBE2A530D (Vidar version 1.6)
    27D4AD97468FA0388BC704A32DD5C5E21E6B1DE76A160FBD2615530C58AA74A6 (Vidar version 1.7)
    155F9F56FCDAB7DD03740656EAA27000AD68F76A4F7B4933FA57416278E909A7 (Vidar version 1.8)

1. Scan for the decoder tail ($pattern) to find decryption trampolines)

    $pattern = {
        E8 ?? ?? ?? ??                   call    vidar_dec_str_trampoline
        C7 05 ?? ?? ?? ?? ?? ?? ?? ??    mov     cs:dword_var, imm32
        48 8D 05 ?? ?? ?? ??             lea     rax, p_output_buffer
        48 83 C4 ??                      add     rsp, imm8
        C3                               ret
    }

2. Collect all CALL xrefs to those trampolines (tail + inline sites)
3. For each site, emulate from the basic-block start to the CALL,
   capture rdx (len) and r9 (output buffer), read the decrypted string
4. Annotate IDA comments and print results to console
"""

import idaapi
import idautils
import idc
import ida_bytes
import ida_funcs
import ida_gdl
import ida_segment
import ida_hexrays
import struct

from unicorn import (
    Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL,
    UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED,
)
from unicorn.x86_const import (
    UC_X86_REG_RSP, UC_X86_REG_RBP,
    UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX,
    UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_EDX, UC_X86_REG_R9,
    UC_X86_REG_R8, UC_X86_REG_R10, UC_X86_REG_R11, UC_X86_REG_R12,
    UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15,
)

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
DO_COMMENTS = True          # write IDA comments (disasm + pseudocode)
DO_RENAME = False           # rename standalone decoder helpers
INCLUDE_INLINE_CALLERS = True  # also cover decrypt calls that aren't in a tail helper
LIMIT = None                # for testing: only process first N sites (None = all)

STACK_BASE = 0x40000000
STACK_SIZE = 0x00200000
RSP0 = STACK_BASE + STACK_SIZE // 2

HEAP_BASE = 0x10000000
HEAP_SIZE = 0x01000000

EMU_COUNT = 4_000_000
EMU_TIMEOUT_US = 15_000_000

MASK32 = 0xFFFFFFFF

# ----------------------------------------------------------------------------
# $pattern (bytes + mask, nibble wildcards supported)
# ----------------------------------------------------------------------------
PATTERN = "E8 ?? ?? ?? ?? C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 83 C4 ?? C3"

def compile_pattern(pat):
    pbytes, pmask = [], []
    for tok in pat.split():
        if tok == '??':
            pbytes.append(0x00)
            pmask.append(0x00)
        elif '?' in tok:
            hi, lo = tok[0], tok[1]
            if lo == '?':
                pbytes.append(int(hi, 16) << 4)
                pmask.append(0xF0)
            else:
                pbytes.append(int(lo, 16))
                pmask.append(0x0F)
        else:
            pbytes.append(int(tok, 16))
            pmask.append(0xFF)
    return bytes(pbytes), bytes(pmask)


def scan_pattern():
    """Return list of EAs where the $pattern tail starts (the CALL/E8)."""
    pbytes, pmask = compile_pattern(PATTERN)
    n = len(pbytes)
    hits = []
    for seg_ea in idautils.Segments():
        seg = ida_segment.getseg(seg_ea)
        if not seg or not (seg.perm & ida_segment.SEGPERM_EXEC):
            continue
        start = seg.start_ea
        end = seg.end_ea
        data = ida_bytes.get_bytes(start, end - start)
        if not data:
            continue
        # anchor on 0xE8 (first opcode of the pattern)
        idx = data.find(b'\xE8')
        while idx != -1 and idx + n <= len(data):
            ok = True
            for j in range(n):
                if (data[idx + j] & pmask[j]) != pbytes[j]:
                    ok = False
                    break
            if ok:
                hits.append(start + idx)
            idx = data.find(b'\xE8', idx + 1)
    return hits


def call_target_of(ea):
    """Resolve E8 rel32 call target at ea."""
    b = ida_bytes.get_bytes(ea, 5)
    if not b or b[0] != 0xE8:
        return idaapi.BADADDR
    disp = struct.unpack('<i', b[1:5])[0]
    return (ea + 5 + disp) & 0xFFFFFFFFFFFFFFFF


# ----------------------------------------------------------------------------
# Basic-block start that contains a given address
# ----------------------------------------------------------------------------
def block_start_for(ea):
    f = ida_funcs.get_func(ea)
    if f is None:
        return idaapi.BADADDR, idaapi.BADADDR
    fc = ida_gdl.FlowChart(f, flags=ida_gdl.FC_PREDS)
    for blk in fc:
        if blk.start_ea <= ea < blk.end_ea:
            return blk.start_ea, f.start_ea
    return f.start_ea, f.start_ea


# ----------------------------------------------------------------------------
# Unicorn engine: map the image once, reuse for every emulation
# ----------------------------------------------------------------------------
class Emu:
    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self._map_image()
        self.uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)
        self.uc.mem_map(HEAP_BASE, HEAP_SIZE, UC_PROT_ALL)
        self._mapped = set()
        self._mapped.update(range(STACK_BASE >> 12, (STACK_BASE + STACK_SIZE) >> 12))
        self._mapped.update(range(HEAP_BASE >> 12, (HEAP_BASE + HEAP_SIZE) >> 12))
        self._mapped.update(range(self.img_base >> 12, (self.img_base + self.img_size) >> 12))
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._hook_unmapped)
        self.uc.hook_add(UC_HOOK_CODE, self._hook_code)
        self.S = {}

    def _map_image(self):
        segs = []
        for s in idautils.Segments():
            seg = ida_segment.getseg(s)
            segs.append((seg.start_ea, seg.end_ea))
        img_min = min(s for s, _ in segs)
        img_max = max(e for _, e in segs)
        base = img_min & ~0xFFF
        size = ((img_max - base) + 0xFFF) & ~0xFFF
        self.img_base = base
        self.img_size = size
        self.uc.mem_map(base, size, UC_PROT_ALL)
        for s, e in segs:
            data = ida_bytes.get_bytes(s, e - s)
            if data:
                self.uc.mem_write(s, data)

    def _hook_unmapped(self, uc, access, address, size, value, user):
        page = address & ~0xFFF
        page_idx = page >> 12
        if page_idx in self._mapped:
            return False
        try:
            uc.mem_map(page, 0x1000, UC_PROT_ALL)
            self._mapped.add(page_idx)
        except UcError:
            return False
        return True

    def _hook_code(self, uc, address, size, user):
        S = self.S
        if address == S['call_ea']:
            S['len'] = uc.reg_read(UC_X86_REG_EDX) & MASK32
            S['out'] = uc.reg_read(UC_X86_REG_R9)
            S['rcx'] = uc.reg_read(UC_X86_REG_RCX)
            S['hit'] = True

    def _reset_regs(self):
        for r in (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                  UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_R8, UC_X86_REG_R9,
                  UC_X86_REG_R10, UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13,
                  UC_X86_REG_R14, UC_X86_REG_R15):
            self.uc.reg_write(r, 0)
        self.uc.reg_write(UC_X86_REG_RSP, RSP0)
        self.uc.reg_write(UC_X86_REG_RBP, RSP0)

    def run(self, begin, stop_ea, call_ea):
        """Emulate [begin, stop_ea); capture args at call_ea. Returns dict."""
        self.S = {'call_ea': call_ea, 'len': None, 'out': None, 'rcx': None,
                  'hit': False, 'err': None}
        self._reset_regs()
        try:
            self.uc.emu_start(begin, stop_ea, timeout=EMU_TIMEOUT_US, count=EMU_COUNT)
        except UcError as e:
            self.S['err'] = str(e)
        except OSError as e:
            self.S['err'] = 'OSError: %s' % e
        try:
            self.S['rax'] = self.uc.reg_read(UC_X86_REG_RAX)
        except (UcError, OSError):
            self.S['rax'] = 0
        return self.S

    def read(self, ea, n):
        try:
            return bytes(self.uc.mem_read(ea, n))
        except UcError:
            return b''


# ----------------------------------------------------------------------------
# Encoding / literal formatting
# ----------------------------------------------------------------------------
def looks_like_utf16(b):
    if len(b) < 4 or (len(b) & 1):
        return False
    pairs = 0
    for i in range(0, len(b), 2):
        lo = b[i]
        hi = b[i + 1]
        if hi != 0:
            return False
        if lo == 0:
            continue
        if lo < 0x09 or (0x0E <= lo < 0x20) or lo > 0x7E:
            return False
        pairs += 1
    return pairs >= 2


def _escape_bytes(s):
    out = []
    for ch in s:
        if ch == 0x5C:
            out.append('\\\\')
        elif ch == 0x22:
            out.append('\\"')
        elif ch == 0x0A:
            out.append('\\n')
        elif ch == 0x0D:
            out.append('\\r')
        elif ch == 0x09:
            out.append('\\t')
        elif ch == 0x00:
            out.append('\\0')
        elif 0x20 <= ch <= 0x7E:
            out.append(chr(ch))
        else:
            out.append('\\x%02x' % ch)
    return ''.join(out)


def _escape_str(text):
    body = []
    for ch in text:
        o = ord(ch)
        if ch == '\\':
            body.append('\\\\')
        elif ch == '"':
            body.append('\\"')
        elif ch == '\n':
            body.append('\\n')
        elif ch == '\r':
            body.append('\\r')
        elif ch == '\t':
            body.append('\\t')
        elif 0x20 <= o <= 0x7E or o > 0x7F:
            body.append(ch)
        else:
            body.append('\\x%02x' % o)
    return ''.join(body)


def format_literal(raw):
    if looks_like_utf16(raw):
        trimmed = raw
        while len(trimmed) >= 2 and trimmed[-2:] == b'\x00\x00':
            trimmed = trimmed[:-2]
        try:
            text = trimmed.decode('utf-16-le')
        except Exception:
            text = trimmed.decode('utf-8', errors='replace')
        return 'L"' + _escape_str(text) + '"'
    trimmed = raw.rstrip(b'\x00')
    try:
        text = trimmed.decode('utf-8')
        return '"' + _escape_str(text) + '"'
    except UnicodeDecodeError:
        return '"' + _escape_bytes(trimmed) + '"'


def extract_field(raw_window, hinted_len):
    """Pick the meaningful slice from the output buffer window."""
    if hinted_len and 0 < hinted_len <= len(raw_window):
        return raw_window[:hinted_len]
    # fall back to terminator detection
    if len(raw_window) >= 4 and raw_window[1] == 0 and raw_window[0] != 0:
        # likely UTF-16: stop at wide NUL
        for i in range(0, len(raw_window) - 1, 2):
            if raw_window[i] == 0 and raw_window[i + 1] == 0:
                return raw_window[:i + 2]
        return raw_window
    j = raw_window.find(b'\x00')
    return raw_window if j < 0 else raw_window[:j + 1]


def is_plausible_string(field):
    if not field:
        return False
    if looks_like_utf16(field):
        return True
    body = field.rstrip(b'\x00')
    if not body:
        return False
    printable = sum(1 for c in body if c == 9 or c == 10 or c == 13 or 0x20 <= c < 0x7F or c >= 0x80)
    return printable / len(body) >= 0.7


# ----------------------------------------------------------------------------
# Comment placement
# ----------------------------------------------------------------------------
class _NearestNode(ida_hexrays.ctree_visitor_t):
    def __init__(self, target):
        ida_hexrays.ctree_visitor_t.__init__(self, ida_hexrays.CV_FAST)
        self.target = target
        self.best_ea = idaapi.BADADDR
        self.best_delta = 1 << 64

    def visit_insn(self, insn):
        if insn.ea != idaapi.BADADDR:
            d = abs(insn.ea - self.target)
            if d < self.best_delta:
                self.best_delta = d
                self.best_ea = insn.ea
        return 0


_HX_OK = None


def set_comment(ea, text):
    global _HX_OK
    idc.set_cmt(ea, text, 0)
    if _HX_OK is None:
        _HX_OK = ida_hexrays.init_hexrays_plugin()
    if not _HX_OK:
        return
    func = ida_funcs.get_func(ea)
    if func is None:
        return
    try:
        cfunc = ida_hexrays.decompile(func.start_ea)
        if cfunc is None:
            return
        finder = _NearestNode(ea)
        finder.apply_to(cfunc.body, None)
        if finder.best_ea == idaapi.BADADDR:
            return
        tl = ida_hexrays.treeloc_t()
        tl.ea = finder.best_ea
        tl.itp = ida_hexrays.ITP_SEMI
        cfunc.set_user_cmt(tl, text)
        cfunc.save_user_cmts()
    except Exception:
        pass


def sanitize_name(literal):
    s = literal
    if s.startswith('L"'):
        s = s[2:]
    s = s.strip('"')
    keep = []
    for ch in s:
        if ch.isalnum():
            keep.append(ch)
        elif ch in ' \\/.:-_':
            keep.append('_')
        if len(keep) >= 40:
            break
    name = ''.join(keep).strip('_')
    return name or 'blob'


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    print('[*] scanning for $pattern decoder tails ...')
    tails = scan_pattern()
    print('    %d tail matches' % len(tails))

    # the CALL target of each tail identifies the decryptor trampoline(s)
    target_freq = {}
    for t in tails:
        tgt = call_target_of(t)
        target_freq[tgt] = target_freq.get(tgt, 0) + 1
    trampolines = sorted(k for k, v in target_freq.items() if v >= 3)
    print('    decryptor trampoline(s): %s'
          % ', '.join('%s(x%d)' % (idc.get_name(t) or hex(t), target_freq[t])
                      for t in trampolines))

    # Build the work list: (call_ea, kind)
    #   'tail'   -> standalone decoder helper found via $pattern
    #   'inline' -> any other CALL xref to a trampoline
    sites = {}  # call_ea -> kind
    for t in tails:
        sites[t] = 'tail'
    if INCLUDE_INLINE_CALLERS:
        for tr in trampolines:
            for xa in idautils.CodeRefsTo(tr, 0):
                if idc.print_insn_mnem(xa) == 'call' and xa not in sites:
                    sites[xa] = 'inline'

    n_tail = sum(1 for k in sites.values() if k == 'tail')
    n_inline = sum(1 for k in sites.values() if k == 'inline')
    print('    sites: %d tail-helpers + %d inline = %d total'
          % (n_tail, n_inline, len(sites)))

    emu = Emu()
    results = []
    fails = []
    order = sorted(sites.keys())
    if LIMIT:
        order = order[:LIMIT]

    for call_ea in order:
        kind = sites[call_ea]
        bb_start, fn_start = block_start_for(call_ea)
        if bb_start == idaapi.BADADDR:
            fails.append((call_ea, 'no func'))
            continue
        stop_ea = (call_ea + 5) & 0xFFFFFFFFFFFFFFFF
        st = emu.run(bb_start, stop_ea, call_ea)

        if not st['hit'] or not st['out']:
            # retry from the function start (handles cross-block arg setup)
            st = emu.run(fn_start, stop_ea, call_ea)

        if not st['hit'] or not st['out']:
            fails.append((call_ea, st.get('err') or 'no capture'))
            continue

        length = st['len'] or 0
        out_ptr = st['out']
        read_n = length if (0 < length <= 8192) else 512
        raw = emu.read(out_ptr, max(read_n, 8))
        field = extract_field(raw, length)
        literal = format_literal(field)
        ok = is_plausible_string(field)

        results.append((call_ea, fn_start, kind, length, literal, ok))

    # ---- annotate ----
    if DO_COMMENTS:
        print('[*] writing IDA comments ...')
        seen_fn = set()
        for call_ea, fn_start, kind, length, literal, ok in results:
            set_comment(call_ea, literal)
            if kind == 'tail' and fn_start not in seen_fn:
                set_comment(fn_start, 'decstr -> %s' % literal)
                seen_fn.add(fn_start)
                if DO_RENAME:
                    base = 'vidar_decstr_' + sanitize_name(literal)
                    nm = base
                    k = 1
                    while idc.get_name_ea_simple(nm) != idaapi.BADADDR:
                        nm = '%s_%d' % (base, k)
                        k += 1
                    idc.set_name(fn_start, nm, idc.SN_NOWARN)

    # ---- dump to console ----
    results.sort(key=lambda r: r[0])
    for call_ea, fn_start, kind, length, literal, ok in results:
        flag = '' if ok else '  ; <suspect>'
        print('0x%X  %-6s  %s%s' % (call_ea, kind, literal, flag))

    print('[*] decoded %d strings (%d suspect), %d failures'
          % (len(results),
             sum(1 for r in results if not r[5]),
             len(fails)))
    if fails:
        print('    first failures: %s'
              % ', '.join('%#x(%s)' % (a, why) for a, why in fails[:10]))

if __name__ == "__main__":
    main()
