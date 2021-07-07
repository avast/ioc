import time
import struct
import socket

HR = 80*'-'
# Rename Flags:
#	32 = SN_AUTO
#	256 = SN_NOWARN
#	2048 = SN_FORCE
FLGS = 32+256+2048

# socket sa_family names
SA_FAMILY_NAMES = [
    'AF_UNSPEC',
    'AF_UNIX',
    'AF_INET',
    'AF_AX25',
    'AF_IPX',
    'AF_APPLETALK',
    'AF_NETROM',
    'AF_BRIDGE',
    'AF_AAL5',
    'AF_X25',
    'AF_INET6',
    'AF_MAX'
]

# known api haseh from reference cobalt strike set
KNOWN_API_NAMES = [
    [0xc99cc96a,'dnsapi.dll_DnsQuery_A'],
    [0x528796c6,'kernel32.dll_CloseHandle'],
    [0xe27d6f28,'kernel32.dll_ConnectNamedPipe'],
    [0xd4df7045,'kernel32.dll_CreateNamedPipeA'],
    [0xfcddfac0,'kernel32.dll_DisconnectNamedPipe'],
    [0x56a2b5f0,'kernel32.dll_ExitProcess'],
    [0x5de2c5aa,'kernel32.dll_GetLastError'],
    [0x0726774c,'kernel32.dll_LoadLibraryA'],
    [0xcc8e00f4,'kernel32.dll_lstrlenA'],
    [0xe035f044,'kernel32.dll_Sleep'],
    [0xbb5f9ead,'kernel32.dll_ReadFile'],
    [0xe553a458,'kernel32.dll_VirtualAlloc'],
    [0x315e2145,'user32.dll_GetDesktopWindow'],
    [0x3b2e55eb,'wininet.dll_HttpOpenRequestA'],
    [0x7b18062d,'wininet.dll_HttpSendRequestA'],
    [0xc69f8957,'wininet.dll_InternetConnectA'],
    [0x0be057b7,'wininet.dll_InternetErrorDlg'],
    [0xa779563a,'wininet.dll_InternetOpenA'],
    [0xe2899612,'wininet.dll_InternetReadFile'],
    [0x869e4675,'wininet.dll_InternetSetOptionA'],
    [0xe13bec74,'ws2_32.dll_accept'],
    [0x6737dbc2,'ws2_32.dll_bind'],
    [0x614d6e75,'ws2_32.dll_closesocket'],
    [0x6174a599,'ws2_32.dll_connect'],
    [0xff38e9b7,'ws2_32.dll_listen'],
    [0x5fc8d902,'ws2_32.dll_recv'],
    [0xe0df0fea,'ws2_32.dll_WSASocketA'],
    [0x006b8029,'ws2_32.dll_WSAStartup']
]
# api block names
X86_API_CALL_BLOCK_NAMES = [
    [0x15,'next_mod'],
    [0x1E,'loop_mod_name'],
    [0x27,'not_lowercase'],
    [0x4A,'get_next_func'],
    [0x54,'loop_func_name'],
    [0x68,'finish'],
    [0x88,'get_next_mod_1'],
    [0x89,'get_next_mod_2']
]
X64_API_CALL_BLOCK_NAMES = [
    [0x21,'next_mod'],
    [0x2D,'loop_mod_name'],
    [0x37,'not_lowercase'],
    [0x6E,'get_next_func'],
    [0x7D,'loop_func_name'],
    [0xB1,'finish'],
    [0xC6,'get_next_mod_1'],
    [0xC7,'get_next_mod_2']
]

# x86 payloads block names
X86_DNS_BLOCK_NAMES = [
    [0x8F,'alloc_space'],
    [0xAF,'load_dnsapi'],
    [0xCA,'process_dnsquery'],
    [0xD8,'dnsquery'],
    [0x10E,'dnsname_fix'],
    [0x10F,'dnsname_fix1'],
    [0x115,'dnsname_ok'],
    [0x145,'goto_process_query'],
    [0x18A,'dnsquery_next_try_or_exit'],
    [0x19E,'sleep_before_next_try'],
    [0x1B5,'get_query_result'],
    [0x1C5,'copy_piece_to_heap'],
    [0x1D9,'check_length'],
    [0x1F9,'prepare_payload'],
    [0x1FB,'jump_to_payload']
]
X86_SMB_BLOCK_NAMES = [
    [0x8F,'alloc_space'],
    [0xAD,'process_pipe'],
    [0x102,'read_next_chunk'],
    [0x12B,'disconnect_pipe'],
    [0x14A,'call_exitprocess'],
    [0x151,'jump_to_payload'],
    [0x155,'goto_process_pipe']
]
X86_TCP_BIND_BLOCK_NAMES = [
    [0x8F,'bind_tcp'],
    [0xD0,'try_connect'],
    [0xF9,'call_exitprocess'],
    [0x100,'recv'],
    [0x10F,'alloc_space'],
    [0x122,'read_more'],
    [0x143,'jump_to_payload']
]
X86_TCP_REVERSE_BLOCK_NAMES = [
    [0x8F,'reverse_tcp'],
    [0xD0,'try_connect'],
    [0xE4,'call_exitprocess'],
    [0xEB,'recv'],
    [0xFA,'alloc_space'],
    [0x10D,'read_more']
]
X86_HTTP_BLOCK_NAMES = [
    [0x8F,'load_wininet'],
    [0xA2,'call_internetopena'],
    [0xB5,'call_internetconnecta'],
    [0xCE,'call_httpopenrequesta'],
    [0xE9,'call_httpsendrequesta'],
    [0x10A,'check_error_1'],
    [0x113,'check_error_2'],
    [0x139,'goto_internetconnecta_1'],
    [0x13E,'goto_httpopenrequesta'],
    [0x2C3,'call_exitprocess'],
    [0x2CA,'alloc_space'],
    [0x2DE,'download_prep'],
    [0x2EA,'download_more'],
    [0x305,'jump_to_payload'],
    [0x307,'goto_internetconnecta_2']
]
X86_HTTPS_BLOCK_NAMES = [
    [0x8F,'load_wininet'],
    [0xA2,'call_internetopena'],
    [0xBA,'call_internetconnecta'],
    [0xD2,'goto_httpopenrequesta_1'],
    [0xD7,'call_httpopenrequesta'],
    [0xED,'call_internetsetoptiona'],
    [0x107,'call_httpsendrequesta'],
    [0x128,'check_error_1'],
    [0x131,'check_error_2'],
    [0x157,'goto_alloc_space'],
    [0x15E,'goto_internetconnecta_1'],
    [0x163,'goto_httpopenrequesta_2'],
    [0x2E8,'call_exitprocess'],
    [0x2EF,'alloc_space'],
    [0x303,'download_prep'],
    [0x30F,'download_more'],
    [0x32A,'jump_to_payload'],
    [0x32C,'goto_internetconnecta_2']
]

# x64 payloads block names
X64_TCP_BIND_BLOCK_NAMES = [
    [0xD2,'bind_tcp'],
    [0x17E,'call_exitprocess'],
    [0x185,'recv'],
    [0x1A5,'alloc_space'],
    [0x1C4,'read_more'],
    [0x1E9,'jump_to_payload']
]
X64_TCP_REVERSE_BLOCK_NAMES = [
    [0xD2,'reverse_tcp'],
    [0x151,'call_exitprocess'],
    [0x158,'recv'],
    [0x178,'alloc_space'],
    [0x197,'read_more']
]
X64_HTTP_BLOCK_NAMES = [
    [0xD2,'load_wininet'],
    [0xEF,'call_internetopena'],
    [0x109,'call_internetconnecta'],
    [0x128,'call_httpopenrequesta'],
    [0x14F,'call_httpsendrequesta'],
    [0x17C,'goto_internetconnecta_1'],
    [0x181,'goto_httpopenrequesta'],
    [0x306,'call_exitprocess'],
    [0x30E,'alloc_space'],
    [0x32A,'download_prep'],
    [0x331,'download_more'],
    [0x35A,'jump_to_payload'],
    [0x365,'goto_internetconnecta_2']
]
X64_HTTPS_BLOCK_NAMES = [
    [0xD2,'load_wininet'],
    [0xEF,'call_internetopena'],
    [0x10C,'call_internetconnecta'],
    [0x12B,'call_httpopenrequesta'],
    [0x152,'call_internetsetoptiona'],
    [0x157,'goto_alloc_space'],
    [0x172,'call_httpsendrequesta'],
    [0x19F,'goto_internetconnecta_1'],
    [0x1A4,'goto_httpopenrequesta'],

    [0x329,'call_exitprocess'],
    [0x331,'alloc_space'],
    [0x34D,'download_prep'],
    [0x354,'download_more'],
    [0x37D,'jump_to_payload'],
    [0x388,'goto_internetconnecta_2']
]


# find all sequences
def find_all_seq(what):
    ret = []
    ea = ida_ida.cvar.inf.min_ea
    while ea != ida_idaapi.BADADDR:
       ea = ida_search.find_binary(ea, ida_idaapi.BADADDR, what, 16, ida_search.SEARCH_DOWN | ida_search.SEARCH_CASE | ida_search.SEARCH_NEXT)
       if ea != ida_idaapi.BADADDR:
           ret.append(ea)
    return ret

# find one sequence
def find_seq(what):
    return ida_search.find_binary(ida_ida.cvar.inf.min_ea, ida_idaapi.BADADDR, what, 16, ida_search.SEARCH_DOWN)

# check payload architecture
def check_arch():
    pattern_x86 = 'FC E8 89 00 00 00 60 89'
    pattern_x64 = 'FC 48 83 E4 F0 E8 C8 00'
    is_x86 = find_seq(pattern_x86)
    if is_x86 != ida_idaapi.BADADDR:
        return ['x86', is_x86]
    is_x64 = find_seq(pattern_x64)
    if is_x64 != ida_idaapi.BADADDR:
        return ['x64', is_x64]
    # unknown
    return ['unknown', -1]

# check payload type by api hash
def check_payload_type():
    pattern_types = [
        # x86
        ['6A C9 9C C9 FF D5', 'DNS'],
        ['45 70 DF D4 FF D5', 'SMB'],
        ['C2 DB 37 67 FF D5', 'TCP_BIND'],
        ['99 A5 74 61 FF D5', 'TCP_REVERSE'],
        ['75 46 9E 86 FF D5', 'HTTPS'],
        ['3A 56 79 A7 FF D5', 'HTTP'],
    ]
    for pattern in pattern_types:
        offset = find_seq(pattern[0])
        if offset != ida_idaapi.BADADDR:
            return pattern[1]
    return 'unknown'

# add comment
def add_comment(ea,cmt):
    ida_bytes.set_cmt(ea,cmt,1)

# create api hashes enum
def enum_create(name):
    idx = ida_enum.get_enum(name)
    if idx == ida_idaapi.BADADDR:
        idx = ida_enum.add_enum(ida_idaapi.BADADDR, name, ida_bytes.hex_flag())
        for crc in KNOWN_API_NAMES:
            enum_add_member(idx,crc[1],crc[0])
        return idx
    else:
        return idx

# add member to enum
def enum_add_member(idx,name,value):
    ida_enum.add_enum_member(idx,name,value,ida_idaapi.BADADDR)

# apply enum
def enum_apply(arch,idx,ea):
    if arch == 'x86':
        return ida_bytes.op_enum(ea, 0, idx, 0) #PUSH value
    elif arch == 'x64':
        return ida_bytes.op_enum(ea, 1, idx, 0) #MOV r, value
    else:
        print('Error: Unknown arch..')
        return -1

# find offset for api hashes
def find_offsets(arch):
    pattern_hash = ''
    if arch == 'x86':
        pattern_hash = '68 ?? ?? ?? ?? FF D5'
    elif arch == 'x64':
        pattern_hash = '41 ?? ?? ?? ?? ?? FF D5'
    else:
        print('Error: Unknown arch..')
        return -1
    return find_all_seq(pattern_hash)

# find api hashes and print api table
def find_api_hashes(arch,idx,start_offset):
    size = 0
    if arch == 'x86':
        size = 1
    elif arch == 'x64':
        size = 2
    else:
        print('Error: Unknown arch..')
        return -1
    offsets = find_offsets(arch)
    hit = False
    print(HR)
    print('Offset\tHash value\t\tAPI name')
    for offset in offsets:
        api_hash = idaapi.get_dword(offset+size)
        for i in range(len(KNOWN_API_NAMES)):
            if KNOWN_API_NAMES[i][0] == api_hash:
                hit = True
                print('%s\t%s\t\t%s' % (hex(offset), hex(api_hash), KNOWN_API_NAMES[i][1]))
                enum_apply(arch,idx,offset)
        if not hit:
            print('[!] unknown hash', hex(api_hash), hex(offset))
        else:
            hit = False
    # exitprocess fix on x64 payloads..
    # tcp reverse
    if arch == 'x64' and ida_bytes.get_dword(start_offset+0x151) == 0xA2B5F068:
        print('%s\t%s\t\t%s' % (hex(start_offset+0x151), '0x56a2b5f0', 'kernel32.dll_ExitProcess'))
        enum_apply('x86',idx,start_offset+0x151)
    # tcp bind
    if arch == 'x64' and ida_bytes.get_dword(start_offset+0x17E) == 0xA2B5F068:
        print('%s\t%s\t\t%s' % (hex(start_offset+0x17E), '0x56a2b5f0', 'kernel32.dll_ExitProcess'))
        enum_apply('x86',idx,start_offset+0x17E)
    print(HR)

# apply predefined function names
def add_func_names(start_offset, func_array):
    for func in func_array:
        ida_name.set_name(start_offset+func[0],func[1],FLGS)

# check and print watermark / customer id
def check_watermark(arch, p_type, start_offset):
    ea_max = ida_ida.cvar.inf.max_ea
    p_size = 0x1000

    if arch == 'x86':
        if p_type == 'DNS':
            p_size = start_offset+0x203
        if p_type == 'SMB':
            p_size = start_offset+0x15A + ida_bytes.get_item_size(start_offset+0x15A)
        if p_type == 'TCP_BIND':
            p_size = start_offset+0x14B + ida_bytes.get_item_size(start_offset+0x14B)
        if p_type == 'TCP_REVERSE':
            p_size = start_offset+0x122 + ida_bytes.get_item_size(start_offset+0x122)
        if p_type == 'HTTP':
            p_size = start_offset+0x30C + ida_bytes.get_item_size(start_offset+0x30C)
        if p_type == 'HTTPS':
            p_size = start_offset+0x331 + ida_bytes.get_item_size(start_offset+0x331)

    if arch == 'x64':
        if p_type == 'TCP_BIND':
            p_size = start_offset+0x1FE + ida_bytes.get_item_size(start_offset+0x1FE)
        if p_type == 'TCP_REVERSE':
            p_size = start_offset+0x1D1 + ida_bytes.get_item_size(start_offset+0x1D1)
        if p_type == 'HTTP':
            p_size = start_offset+0x36A + ida_bytes.get_item_size(start_offset+0x36A)
        if p_type == 'HTTPS':
            p_size = start_offset+0x38D + ida_bytes.get_item_size(start_offset+0x38D)

    if ea_max > p_size:
        ida_name.set_name(p_size,'watermark',FLGS)
        ida_bytes.create_byte(p_size, ea_max-p_size)
        wb = ida_bytes.get_bytes(p_size, ea_max-p_size)
        wf = '\\x'.join(format(x, '02x') for x in wb)
        print('watermark:\t\t\\x' + wf)
    else:
        print('watermark:\t\tnot found')

# set FUNC_NORET flags
def set_noret_flag(ea):
    func = ida_funcs.get_func(ea)
    if not func:
        print('0x%x get_func error!' % ea)
        return 0
    else:
        func.flags = 0x1 #FUNC_NORET
        ida_funcs.update_func(func)
    return 1


def payload_analysis():
    # check x86 / x64
    arch, start_offset = check_arch()
    if start_offset == -1:
        print('Payload not found..')
        return 0
    # check payload type
    payload_type = check_payload_type()
    if payload_type == 'unknown':
        print('Unknown payload type..')
        return 0

    # check execution environments architecture
    # https://www.programcreek.com/python/example/85151/idaapi.get_inf_structure
    env = idaapi.dbg_get_registers()
    if env[17][0] == 'RAX' and arch == 'x86':
        print('This is x86 payload, please load it with IDA 32-bit version.')
        return 0

    if env[17][0] == 'EAX' and arch == 'x64':
        print('This is x64 payload, please load it with IDA 64-bit version.')
        return 0

    print(HR)
    print('Start offset:\t0x%x' % start_offset)
    print('Architecture:\t%s' % arch)
    print('Payload type:\t%s' % payload_type)
    print(HR)

    # create enums
    idx = enum_create('Cobalt_Strike')
    # undefine all
    ida_bytes.del_items(start_offset,FF_UNK,0x1000)
    # add 'start' entry on 0x0
    ida_entry.add_entry(0,start_offset,'payload_start',1)
    # make code and wait for result
    idaapi.auto_wait()


    # x86
    if arch == 'x86':
        # set end of payload_start function
        ida_funcs.set_func_end(start_offset, start_offset+0x6)
        # set api_call function
        ida_funcs.add_func(start_offset+0x6,ida_idaapi.BADADDR)
        ida_name.set_name(start_offset+0x6,'api_call',FLGS)
        # rename local names in api_call function
        add_func_names(start_offset, X86_API_CALL_BLOCK_NAMES)
        add_comment(start_offset+ 0x86,'Jump into the required function')

        if payload_type == 'DNS':
            add_func_names(start_offset, X86_DNS_BLOCK_NAMES)
            # set FUNC_NORET flag to process_dnsquery function
            set_noret_flag(start_offset+0xCA)
            # comment DnsQuery_A parameters
            dns_record_type =  ida_bytes.get_byte(start_offset+0x12C)
            dns_query_options = struct.unpack('<H', ida_bytes.get_bytes(start_offset+0x127,2,1))[0]
            if dns_record_type == 0x10:
                dns_record_type = 'wType: 0x0010 | DNS_TYPE_TEXT'
            else:
                dns_record_type = 'wType: 0x%04x (custom value)' % dns_record_type
            if dns_query_options == 0x248:
                dns_query_options = 'Options: 0x0248 | DNS_QUERY_BYPASS_CACHE, DNS_QUERY_NO_HOSTS_FILE, DNS_QUERY_RETURN_MESSAGE'
            else:
                dns_query_options = 'Options: 0x%04x (custom value)' % dns_query_options
            add_comment(start_offset+0x12B, dns_record_type)
            add_comment(start_offset+0x126, dns_query_options)
            # fix config blog data
            ida_bytes.del_items(start_offset+0x14A,FF_UNK,0x3F)
            # create dnsname string
            ida_bytes.create_strlit(start_offset+0x14B,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x14B,'dns_name',FLGS)
            dnsname = ida_bytes.get_strlit_contents(start_offset+0x14B,ida_bytes.get_item_size(start_offset+0x14B),ida_nalt.STRTYPE_TERMCHR)
            print('dns_name:\t\t%s' % dnsname.decode('UTF-8'))
            # convert rest of config blob to bytes data
            s_size = ida_bytes.get_item_size(start_offset+0x14B)
            ida_bytes.create_byte(start_offset+0x14B+s_size, start_offset+0x18A-0x14B-s_size)
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'SMB':
            # fix http_c2 and watermark blob
            ida_funcs.set_func_end(start_offset+0x155, start_offset+0x15A)
            idaapi.auto_wait()
            ida_bytes.del_items(start_offset+0x15A,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x100)
            idaapi.auto_wait()
            # comment CreateNamedPipeA parameters
            smb_max_instances = ida_bytes.get_byte(start_offset+0xBD)
            smb_pipe_mode = ida_bytes.get_byte(start_offset+0xBF)
            smb_open_mode = ida_bytes.get_byte(start_offset+0xC1)
            if smb_max_instances == 1:
                smb_max_instances = 'nMaxInstances: 0x%02x' % smb_max_instances
            else:
                smb_max_instances = 'nMaxInstances: 0x%02x  (custom value)' % smb_max_instances
            if smb_pipe_mode == 6:
                smb_pipe_mode = 'dwPipeMode: 0x%02x  | PIPE_TYPE_MESSAGE, PIPE_READMODE_MESSAGE' % smb_pipe_mode
            else:
                smb_pipe_mode = 'dwPipeMode: 0x%02x  (custom value)' % smb_pipe_mode
            if smb_open_mode == 3:
                smb_open_mode = 'dwOpenMode: 0x%02x  | PIPE_ACCESS_DUPLEX' % smb_open_mode
            else:
                smb_open_mode = 'dwOpenMode: 0x%02x  (custom value)' % smb_open_mode
            add_comment(start_offset+0xBC, smb_max_instances)
            add_comment(start_offset+0xBE, smb_pipe_mode)
            add_comment(start_offset+0xC0, smb_open_mode)
            # create pipe string
            ida_bytes.create_strlit(start_offset+0x15A,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x15A,'pipe',FLGS)
            p_size = ida_bytes.get_item_size(start_offset+0x15A)
            # apply predefined function names
            add_func_names(start_offset, X86_SMB_BLOCK_NAMES)
            # print pipe value
            pipe = ida_bytes.get_strlit_contents(start_offset+0x15A,p_size,ida_nalt.STRTYPE_TERMCHR)
            print('pipe:\t\t%s' % pipe.decode('UTF-8'))
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'TCP_BIND' or payload_type == 'TCP_REVERSE':
            # parse IP
            ip = '%d.%d.%d.%d' % struct.unpack('BBBB', ida_bytes.get_bytes(start_offset+0xC5,4,1))
            # parse sa_family
            sa_family_value = ida_bytes.get_word(start_offset+0xCA)
            try:
                sa_family = SA_FAMILY_NAMES[sa_family_value]
            except KeyError:
                sa_family = 'unknown'
            # parse port
            port = '%i' % struct.unpack('>H', ida_bytes.get_bytes(start_offset+0xCC,2,1))[0]
            # print values
            print('sin_addr:\t\t%s' % ip)
            print('sin_port:\t\t%s' % port)
            print('sa_family:\t\t%s' % sa_family)
            # apply predefined function names
            if payload_type == 'TCP_BIND':
                add_func_names(start_offset,X86_TCP_BIND_BLOCK_NAMES)
            else:
                add_func_names(start_offset,X86_TCP_REVERSE_BLOCK_NAMES)
            # add comments
            add_comment(start_offset+0xC4, 'sin_ip: '+ip)
            add_comment(start_offset+0xC9,'sin_port: '+port+'\nsa_family: '+sa_family)
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'HTTP':
            # set FUNC_NORET flags
            set_noret_flag(start_offset+0x8F)
            set_noret_flag(start_offset+0xB5)
            set_noret_flag(start_offset+0xCE)
            set_noret_flag(start_offset+0xE9)
            # fix config blog data
            ida_bytes.del_items(start_offset+0x143,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x17F)
            idaapi.auto_wait()
            idc.create_insn(start_offset+0x2c3)
            # create url_query string
            ida_bytes.create_strlit(start_offset+0x143,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x143,'request_query',FLGS)
            q_size = ida_bytes.get_item_size(start_offset+0x143)
            for i in range(0x50-q_size+1):
                ida_bytes.create_byte(start_offset+0x143+q_size,i)
            idaapi.auto_wait()
            # create request headerer string
            ida_bytes.create_strlit(start_offset+0x193,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x193,'request_header',FLGS)
            u_size = ida_bytes.get_item_size(start_offset+0x193)
            for i in range(0x12F-u_size+1):
                ida_bytes.create_byte(start_offset+0x193+u_size,i)
            idaapi.auto_wait()
            # fix http_c2 and watermark blob
            ida_funcs.set_func_end(start_offset+0x307, start_offset+0x30C)
            ida_bytes.del_items(start_offset+0x30C,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x100)
            idaapi.auto_wait()
            # create http_c2 string
            ida_bytes.create_strlit(start_offset+0x30C,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x30C,'request_addr',FLGS)
            h_size = ida_bytes.get_item_size(start_offset+0x30C)
            # get port value from InternetConnectA API
            port = ida_bytes.get_dword(start_offset+0xBF)
            add_comment(start_offset+0xBE, 'port: '+str(port))
            # apply predefined function names
            add_func_names(start_offset,X86_HTTP_BLOCK_NAMES)
            # print full c2 url and user-agent strings
            http_c2 = ida_bytes.get_strlit_contents(start_offset+0x30C,h_size,ida_nalt.STRTYPE_TERMCHR)
            url_query = ida_bytes.get_strlit_contents(start_offset+0x143,q_size,ida_nalt.STRTYPE_TERMCHR)
            request_header = ida_bytes.get_strlit_contents(start_offset+0x193,u_size,ida_nalt.STRTYPE_TERMCHR).decode('utf-8').strip().split('\r\n')
            print('request_addr:\t%s' % http_c2.decode('UTF-8'))
            print('request_query:\t%s' % url_query.decode('UTF-8'))
            print('request_port:\t%i' % port)
            hdrs = ''
            for h in request_header:
                if h != '':
                    hdrs += '\t%s\n\t' % h
            print('request_header:%s' % hdrs[:-2])
            print(HR)
            print('full c2 ulr: \thttp://%s:%i%s' % (http_c2.decode('UTF-8'), port, url_query.decode('UTF-8')))
            print(HR)
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'HTTPS':
            # set FUNC_NORET flags
            set_noret_flag(start_offset+0x8F)
            set_noret_flag(start_offset+0xBA)
            set_noret_flag(start_offset+0xD7)
            # fix config blog data
            ida_funcs.set_func_end(start_offset+0x163, start_offset+0x168)
            idaapi.auto_wait()
            ida_bytes.del_items(start_offset+0x168,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x17F)
            idaapi.auto_wait()
            ida_ua.create_insn(start_offset+0x2E8)
            if ida_funcs.get_func(start_offset+0x2E8) == None:
                ida_funcs.add_func(start_offset+0x2E8)
                set_noret_flag(start_offset+0x2E8)
            # create url_query string
            ida_bytes.create_strlit(start_offset+0x168,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x168,'request_query',FLGS)
            q_size = ida_bytes.get_item_size(start_offset+0x168)
            for i in range(0x50-q_size+1):
                ida_bytes.create_byte(start_offset+0x168+q_size,i)
            idaapi.auto_wait()
            # create request headerer string
            ida_bytes.create_strlit(start_offset+0x1B8,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x1B8,'request_header',FLGS)
            u_size = ida_bytes.get_item_size(start_offset+0x1B8)
            for i in range(0x12F-u_size+1):
                ida_bytes.create_byte(start_offset+0x1B8+u_size,i)
            idaapi.auto_wait()
            # fix http_c2 and watermark blob
            ida_funcs.set_func_end(start_offset+0x32C, start_offset+0x331)
            ida_bytes.del_items(start_offset+0x331,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x100)
            idaapi.auto_wait()
            # create http_c2 string
            ida_bytes.create_strlit(start_offset+0x331,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x331,'request_addr',FLGS)
            h_size = ida_bytes.get_item_size(start_offset+0x331)
            # get port value from InternetConnectA API
            port = ida_bytes.get_dword(start_offset+0xC4)
            add_comment(start_offset+0xC3, 'port: '+str(port))
            # apply predefined function names
            add_func_names(start_offset,X86_HTTPS_BLOCK_NAMES)
            # print full c2 url and user-agent strings
            http_c2 = ida_bytes.get_strlit_contents(start_offset+0x331,h_size,ida_nalt.STRTYPE_TERMCHR)
            url_query = ida_bytes.get_strlit_contents(start_offset+0x168,q_size,ida_nalt.STRTYPE_TERMCHR)
            request_header = ida_bytes.get_strlit_contents(start_offset+0x1B8,u_size,ida_nalt.STRTYPE_TERMCHR).decode('utf-8').strip().split('\r\n')
            print('request_addr:\t%s' % http_c2.decode('UTF-8'))
            print('request_query:\t%s' % url_query.decode('UTF-8'))
            print('request_port:\t%i' % port)
            hdrs = ''
            for h in request_header:
                if h != '':
                    hdrs += '\t%s\n\t' % h
            print('request_header:%s' % hdrs[:-2])
            print(HR)
            print('full c2 ulr: \thttps://%s:%i%s' % (http_c2.decode('UTF-8'), port, url_query.decode('UTF-8')))
            print(HR)
            # check watermark
            check_watermark(arch,payload_type,start_offset)


    # x64
    if arch == 'x64':
        # set end of payload_start function
        ida_funcs.set_func_end(start_offset+0x0, start_offset+0xA)
        # set api_call function
        ida_funcs.add_func(start_offset+0xA,ida_idaapi.BADADDR)
        ida_name.set_name(start_offset+0xA,'api_call',FLGS)
        # rename local names in api_call function
        add_func_names(start_offset, X64_API_CALL_BLOCK_NAMES)
        add_comment(start_offset+0xC4,'Jump into the required function')

        if payload_type == 'TCP_BIND' or payload_type == 'TCP_REVERSE':
            # parse IP
            ip = '%d.%d.%d.%d' % struct.unpack('BBBB', ida_bytes.get_bytes(start_offset+0xF2,4,1))
            # parse sa_family
            sa_family_value = ida_bytes.get_word(start_offset+0xEE)
            try:
                sa_family = SA_FAMILY_NAMES[sa_family_value]
            except KeyError:
                sa_family = 'unknown'
            # parse port
            port = '%i' % struct.unpack('>H', ida_bytes.get_bytes(start_offset+0xF0,2,1))[0]
            # print values
            print('sin_addr:\t\t%s' % ip)
            print('sin_port:\t\t%s' % port)
            print('sa_family:\t\t%s' % sa_family)
            # apply predefined function names
            if payload_type == 'TCP_BIND':
                add_func_names(start_offset,X64_TCP_BIND_BLOCK_NAMES)
            else:
                add_func_names(start_offset,X64_TCP_REVERSE_BLOCK_NAMES)
            # add comments
            add_comment(start_offset+0xEC, 'sin_ip: '+ip+'\nsin_port: '+port+'\nsa_family: '+sa_family)
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'HTTP':
            # set end of payload_start function
            ida_funcs.set_func_end(start_offset+0x0, start_offset+0xA)
            # set api_call function
            ida_funcs.add_func(start_offset+0xA,ida_idaapi.BADADDR)
            ida_name.set_name(start_offset+0xA,'api_call',FLGS)
            # rename local names in api_call function
            add_func_names(start_offset, X64_API_CALL_BLOCK_NAMES)
            add_comment(start_offset+0xC4,'Jump into the required function')
            # fix config blog data
            ida_bytes.del_items(start_offset+0x186,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x180)
            idaapi.auto_wait()
            # create url_query string
            ida_bytes.create_strlit(start_offset+0x186,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x186,'request_query',FLGS)
            q_size = ida_bytes.get_item_size(start_offset+0x186)
            for i in range(0x50-q_size+1):
                ida_bytes.create_byte(start_offset+0x186+q_size,i)
            idaapi.auto_wait()
            # create request headerer string
            ida_bytes.create_strlit(start_offset+0x1D6,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x1D6,'request_header',FLGS)
            u_size = ida_bytes.get_item_size(0x1D6)
            for i in range(start_offset+0x12F-u_size+1):
                ida_bytes.create_byte(start_offset+0x1D6+u_size,i)
            idaapi.auto_wait()
            # fix http_c2 and watermark blob
            ida_funcs.set_func_end(start_offset+0x365, start_offset+0x36A)
            idaapi.auto_wait()
            ida_bytes.del_items(start_offset+0x36A,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x100)
            idaapi.auto_wait()
            # create http_c2 string
            ida_bytes.create_strlit(start_offset+0x36A,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x36A,'request_addr',FLGS)
            h_size = ida_bytes.get_item_size(start_offset+0x36A)
            # get port value from InternetConnectA API
            port = ida_bytes.get_dword(0x10F)
            add_comment(start_offset+0x10D, 'port: '+str(port))
            # apply predefined function names
            add_func_names(start_offset,X64_HTTP_BLOCK_NAMES)
            # print full c2 url and user-agent strings
            http_c2 = ida_bytes.get_strlit_contents(start_offset+0x36A,h_size,ida_nalt.STRTYPE_TERMCHR)
            url_query = ida_bytes.get_strlit_contents(start_offset+0x186,q_size,ida_nalt.STRTYPE_TERMCHR)
            request_header = ida_bytes.get_strlit_contents(start_offset+0x1D6,u_size,ida_nalt.STRTYPE_TERMCHR).decode('utf-8').strip().split('\r\n')
            print('request_addr:\t%s' % http_c2.decode('UTF-8'))
            print('request_query:\t%s' % url_query.decode('UTF-8'))
            print('request_port:\t%i' % port)
            hdrs = ''
            for h in request_header:
                if h != '':
                    hdrs += '\t%s\n\t' % h
            print('request_header:%s' % hdrs[:-2])
            print(HR)
            print('full c2 ulr: \thttp://%s:%i%s' % (http_c2.decode('UTF-8'), port, url_query.decode('UTF-8')))
            print(HR)
            # check watermark
            check_watermark(arch,payload_type,start_offset)

        if payload_type == 'HTTPS':
            # set end of payload_start function
            ida_funcs.set_func_end(start_offset+0x0, start_offset+0xA)
            # set api_call function
            ida_funcs.add_func(start_offset+0xA,ida_idaapi.BADADDR)
            ida_name.set_name(start_offset+0xA,'api_call',FLGS)
            # rename local names in api_call function
            add_func_names(start_offset, X64_API_CALL_BLOCK_NAMES)
            add_comment(start_offset+0xC4,'Jump into the required function')
            # fix config blog data
            ida_bytes.del_items(start_offset+0x1A9,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x17F)
            idaapi.auto_wait()
            # create url_query string
            ida_bytes.create_strlit(start_offset+0x1A9,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x1A9,'request_query',FLGS)
            q_size = ida_bytes.get_item_size(start_offset+0x1A9)
            for i in range(0x50-q_size+1):
                ida_bytes.create_byte(start_offset+0x1A9+q_size,i)
            idaapi.auto_wait()
            # create request headerer string
            ida_bytes.create_strlit(start_offset+0x1F9,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x1F9,'request_header',FLGS)
            u_size = ida_bytes.get_item_size(start_offset+0x1F9)
            for i in range(0x12F-u_size+1):
                ida_bytes.create_byte(start_offset+0x1F9+u_size,i)
            idaapi.auto_wait()
            # fix http_c2 and watermark blob
            ida_funcs.set_func_end(start_offset+0x388, start_offset+0x38D)
            idaapi.auto_wait()
            ida_bytes.del_items(start_offset+0x38D,DELIT_SIMPLE|DELIT_EXPAND|DELIT_DELNAMES,0x100)
            idaapi.auto_wait()
            # create http_c2 string
            ida_bytes.create_strlit(start_offset+0x38D,0,ida_nalt.STRTYPE_TERMCHR)
            ida_name.set_name(start_offset+0x38D,'request_addr',FLGS)
            h_size = ida_bytes.get_item_size(start_offset+0x38D)
            # get port value from InternetConnectA API
            port = ida_bytes.get_dword(start_offset+0x112)
            add_comment(start_offset+0x110, 'port: '+str(port))
            # apply predefined function names
            add_func_names(start_offset,X64_HTTPS_BLOCK_NAMES)
            # print full c2 url and user-agent strings
            http_c2 = ida_bytes.get_strlit_contents(start_offset+0x38D,h_size,ida_nalt.STRTYPE_TERMCHR)
            url_query = ida_bytes.get_strlit_contents(start_offset+0x1A9,q_size,ida_nalt.STRTYPE_TERMCHR)
            request_header = ida_bytes.get_strlit_contents(start_offset+0x1F9,u_size,ida_nalt.STRTYPE_TERMCHR).decode('utf-8').strip().split('\r\n')
            print('request_addr:\t%s' % http_c2.decode('UTF-8'))
            print('request_query:\t%s' % url_query.decode('UTF-8'))
            print('request_port:\t%i' % port)
            hdrs = ''
            for h in request_header:
                if h != '':
                    hdrs += '\t%s\n\t' % h
            print('request_header:%s' % hdrs[:-2])
            print(HR)
            print('full c2 ulr: \thttps://%s:%i%s' % (http_c2.decode('UTF-8'), port, url_query.decode('UTF-8')))
            print(HR)
            # check watermark
            check_watermark(arch,payload_type,start_offset)


    find_api_hashes(arch,idx,start_offset)
    return 1


if __name__ == '__main__':
    payload_analysis()
