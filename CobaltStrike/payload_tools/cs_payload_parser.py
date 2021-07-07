import struct
import re
import sys
from pathlib import Path

### Constants
VERSION = 1.0
# Default API hashes used in raw payloads
PAYLOAD_API_HASHES = {
    0xc99cc96a : 'dnsapi.dll_DnsQuery_A',
    0x528796c6 : 'kernel32.dll_CloseHandle',
    0xe27d6f28 : 'kernel32.dll_ConnectNamedPipe',
    0xd4df7045 : 'kernel32.dll_CreateNamedPipeA',
    0xfcddfac0 : 'kernel32.dll_DisconnectNamedPipe',
    0x56a2b5f0 : 'kernel32.dll_ExitProcess',
    0x5de2c5aa : 'kernel32.dll_GetLastError',
    0x0726774c : 'kernel32.dll_LoadLibraryA',
    0xcc8e00f4 : 'kernel32.dll_lstrlenA',
    0xe035f044 : 'kernel32.dll_Sleep',
    0xbb5f9ead : 'kernel32.dll_ReadFile',
    0xe553a458 : 'kernel32.dll_VirtualAlloc',
    0x315e2145 : 'user32.dll_GetDesktopWindow',
    0x3b2e55eb : 'wininet.dll_HttpOpenRequestA',
    0x7b18062d : 'wininet.dll_HttpSendRequestA',
    0xc69f8957 : 'wininet.dll_InternetConnectA',
    0x0be057b7 : 'wininet.dll_InternetErrorDlg',
    0xa779563a : 'wininet.dll_InternetOpenA',
    0xe2899612 : 'wininet.dll_InternetReadFile',
    0x869e4675 : 'wininet.dll_InternetSetOptionA',
    0xe13bec74 : 'ws2_32.dll_accept',
    0x6737dbc2 : 'ws2_32.dll_bind',
    0x614d6e75 : 'ws2_32.dll_closesocket',
    0x6174a599 : 'ws2_32.dll_connect',
    0xff38e9b7 : 'ws2_32.dll_listen',
    0x5fc8d902 : 'ws2_32.dll_recv',
    0xe0df0fea : 'ws2_32.dll_WSASocketA',
    0x006b8029 : 'ws2_32.dll_WSAStartup'
}
# Raw payloads x86/x64 patterns
PAYLOAD_ARCH_PATTERNS = {
    b'\xFC\xE8\x89\x00\x00\x00\x60\x89' : 'x86',
    b'\xFC\x48\x83\xE4\xF0\xE8\xC8\x00' : 'x64'
}
# Socket sa_family names
SA_FAMILY_NAMES = {
	0x00 : 'AF_UNSPEC',
	0x01 : 'AF_UNIX',
	0x02 : 'AF_INET',
	0x03 : 'AF_AX25',
	0x04 : 'AF_IPX',
	0x05 : 'AF_APPLETALK',
	0x06 : 'AF_NETROM',
	0x07 : 'AF_BRIDGE',
	0x08 : 'AF_AAL5',
	0x09 : 'AF_X25',
	0x0a : 'AF_INET6',
	0x0b : 'AF_MAX'
}
# Raw payload verification table
VERIFY_TABLE = {
    'API block x86': {
        0x0006: b'\x60\x89\xE5\x31\xD2',
        0x0027: b'\xC1\xCF\x0D',
        0x004d: b'\x8B\x34\x8B',
        0x0086: b'\xFF\xE0'
    },
    'API block x64': {
        0x000a: b'\x41\x51\x41\x50\x52\x51\x56\x48\x31\xD2',
        0x0037: b'\x41\xC1\xC9\x0D',
        0x0073: b'\x41\x8B\x34\x88',
        0x00c4: b'\xFF\xE0'
    },
    'DNS stager x86': {
        0x008f: b'\x5D\x31\xC0\x6A\x40\xB4\x10\x68\x00\x10\x00\x00',
        0x00d8: b'\x89\xF8\x83\xE8\x40\x40\x80\xFB\x7A',
        0x0197: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x01ed: b'\x3D\xFF\x00\x00\x00'
    },
    'SMB stager x86': {
        0x008f: b'\x5D\x31\xC0\x6A\x40\x68\x00\x10\x00\x00',
        0x00e2: b'\x89\xE6\x83\xC6\x04\x89\xE2',
        0x014a: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x0151: b'\xFF\x64'
    },

    'TCP bind x86': {
        0x008f: b'\x5D\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5F\x54\x68\x4C\x77\x26\x07\xFF\xD5',
        0x00c1: b'\x97\x31\xDB',
        0x00f9: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x014b: b'\xC3'
    },
    'TCP bind x64': {
        0x00d2: b'\x5D\x49\xBE\x77\x73\x32\x5F\x33\x32\x00\x00\x41\x56\x49\x89\xE6\x48\x81\xEC\xA0\x01\x00\x00',
        0x0140: b'\x41\xBA\xC2\xDB\x37\x67',
        0x01b0: b'\x48\x89\xF2\x48\x31\xC9',
        0x01fb: b'\x41\xFF\xE7'
    },
    'TCP reverse x86': {
        0x008f: b'\x5D\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5F\x54\x68\x4C\x77\x26\x07\xFF\xD5',
        0x00c1: b'\x97\x6A\x05',
        0x00e4: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x0121: b'\xC3'
    },
    'TCP reverse x64': {
        0x00d2: b'\x5D\x49\xBE\x77\x73\x32\x5F\x33\x32\x00\x00\x41\x56\x49\x89\xE6\x48\x81\xEC\xA0\x01\x00\x00',
        0x0140: b'\x41\xBA\x99\xA5\x74\x61',
        0x0197: b'\x4D\x31\xC9\x49\x89\xF0',
        0x01ce: b'\x41\xFF\xE7'
    },
    'HTTP stager x86': {
        0x008f: b'\x5D\x68\x6E\x65\x74\x00\x68\x77\x69\x6E\x69\x54',
        0x00ce: b'\x5B\x31\xD2',
        0x02c3: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x0306: b'\xC3'
    },
    'HTTP stager x64': {
        0x00d2: b'\x5D\x6A\x00\x49\xBE\x77\x69\x6E\x69\x6E\x65\x74\x00\x41\x56',
        0x012c: b'\x48\x31\xD2',
        0x0306: b'\x41\xBE\xF0\xB5\xA2\x56\xFF\xD5',
        0x0364: b'\xC3'
    },
    'HTTPS stager x86': {
        0x008f: b'\x5D\x68\x6E\x65\x74\x00\x68\x77\x69\x6E\x69\x54',
        0x00d7: b'\x5B\x31\xD2',
        0x02e8: b'\x68\xF0\xB5\xA2\x56\xFF\xD5',
        0x032b: b'\xC3'
    },
    'HTTPS stager x64': {
        0x00d2: b'\x5D\x6A\x00\x49\xBE\x77\x69\x6E\x69\x6E\x65\x74\x00\x41\x56',
        0x012f: b'\x48\x31\xD2',
        0x0329: b'\x41\xBE\xF0\xB5\xA2\x56\xFF\xD5',
        0x0387: b'\xC3'
    }
}
# checksum8 names
CHECKSUM8_NAMES = {
	0x5c : 'Beacon_x86',
	0x5d : 'Beacon_x64',
	0x50 : 'Python',
	0x58 : 'Java',
	0x62 : 'Existing session',
	0x5f : 'New stageless session',
}
# decorations
HR = '-'*80


### Helper functions
# URL checksum8
def checksum8(s):
    n = 'invalid'
    if s.startswith('/'):
        s = s[1:]
    if len(s) >= 4:
        checksum = sum([ord(ch) for ch in s]) % 0x100
        try:
            n = CHECKSUM8_NAMES[checksum]
        except KeyError:
            pass
    return n

# Get string from offset or buffer
def get_str(data, start, end=None):
    if not end:
        rng = data[start:]
    else:
        rng = data[start:end]
    m = re.search(b'[ -~\r\n]{3,}\x00', rng)
    if m:
        return m.group(0)[:-1].decode('utf-8')
    return 'not found'

# Print payload API list
def print_api_functions(data, offset):
    output = 'Payload API list:\n'
    output += 'Offset  | Hash value  | API name'
    for api in data:
        output += '\n0x%04x  | 0x%08x  | %s' % (offset+api[0], api[1], api[2])
    output += '\n%s' % HR
    return output

# Get Customer ID / Watermark data
def get_watermark(data, off):
    str_len = 0
    m = re.search(b'[ -~]{3,}\x00', data[off:])
    if m:
        str_len = len(m.group())
    if str_len > 0:
        return struct.unpack_from('>I', data, off+str_len)[0]
    return 0

# Verify raw payload structure
def verify_payload_data(data, payload_type, arch='x86'):
    api_block = 'API block %s' % arch
    payload_block = '%s %s' %  (payload_type, arch)
    for vblock in [api_block, payload_block]:
        for offset, pattern in VERIFY_TABLE[vblock].items():
            buff = data[offset:offset+len(pattern)]
            if buff != pattern:
                return False
    return True

# Create curl command line for HTTP/HTTPS payloads
def create_curl_comand(data):
    output = ''
    if len(data) == 6:
        verify_query, request_type, request_addr, request_port, request_query, request_header = data
        url = '%s://%s:%s%s' % (request_type, request_addr, request_port, request_query)
        request_header = request_header.split('\r\n')
        header = ''.join('-H "%s" ' % h for h in request_header[:-1])
        if verify_query == 'invalid':
            next_stage_type = 'download'
        else:
            next_stage_type = '%s' % verify_query.replace(' ', '_').lower()
        output = 'Curl download command:\ncurl -o %s.bin %s%s\n%s\n' % (next_stage_type,header,url,HR)
    return output

# Remove utf-16-le encoding
def fix_utf16(buff):
    r = re.compile(b'^([\x00-\xff]\x00){200,}')
    m = re.search(r,buff)
    if m:
        buff = re.sub(b'([\x00-\xff])\x00', rb'\1', buff)
    return buff

### Parser functions
# Get payload architecture and start offset
def get_payload_arch(data):
    items = PAYLOAD_ARCH_PATTERNS.items()
    r = re.compile(b'|'.join(k for k, v in items))
    m = re.search(r, data)
    if m:
        payload_start = m.start()
        arch_type = PAYLOAD_ARCH_PATTERNS[m.group()]
        return payload_start, arch_type
    else:
        return -1, None

# Parse payload API functions
def parse_api_functions(data, arch):
    api_list = []
    op_size = 1
    r = ''
    if arch == 'x86':
        r = re.compile(b'\x68[\x00-\xff]{4}\xff\xd5')
    elif arch == 'x64':
        r = re.compile(b'\x41[\x00-\xff]{5}\xff\xd5')
        op_size = 2
    m = re.finditer(r, data)
    for h in m:
        offset = h.start()+op_size
        api_hash = struct.unpack_from('<I', data,offset)[0]
        try:
            api_name = PAYLOAD_API_HASHES[api_hash]
        except KeyError:
            api_name = 'UNKNOWN'
        api_list.append([offset, api_hash, api_name])
    return api_list

# Get payload type from used API hashes
def get_payload_type(data):
    payload_type = 'unknown'
    for api in data:
        api_hash = api[1]
        if api_hash == 0x6737dbc2:     # ws2_32.dll_bind
            payload_type = 'TCP bind'
        elif api_hash == 0x6174a599:   # ws2_32.dll_connect
            payload_type = 'TCP reverse'
        elif api_hash == 0xc99cc96a:   # dnsapi.dll_DnsQuery_A
            payload_type = 'DNS stager'
        elif api_hash == 0xd4df7045:   # kernel32.dll_CreateNamedPipeA
            payload_type = 'SMB stager'
        elif api_hash == 0xa779563a:   # wininet.dll_InternetOpenA
            payload_type = 'HTTP stager'
        elif api_hash == 0x869e4675:   # wininet.dll_InternetSetOptionA
            payload_type = 'HTTPS stager'
    return payload_type

# Parse watermark from raw payload
def parse_watermark(data, payload_type, arch='x86'):
    watermark = 0
    payload_size = len(data)

    if payload_type.startswith('DNS') and payload_size > 0x203:
        watermark = struct.unpack_from('>I', data, 0x203)[0]
    if payload_type.startswith('SMB') and payload_size > 0x15a:
        watermark = get_watermark(data, 0x15a)
    if payload_type == 'TCP bind' and arch == 'x86' and payload_size > 0x14c:
        watermark = struct.unpack_from('>I', data, 0x14c)[0]
    if payload_type == 'TCP bind' and arch == 'x64' and payload_size > 0x1fe:
        watermark = struct.unpack_from('>I', data, 0x1fe)[0]
    if payload_type == 'HTTP stager' and arch == 'x86' and payload_size > 0x30c:
        watermark = get_watermark(data, 0x30c)
    if payload_type == 'HTTP stager' and arch == 'x64' and payload_size > 0x36a:
        watermark = get_watermark(data, 0x36a)
    if payload_type == 'HTTPS stager' and arch == 'x86' and payload_size > 0x331:
        watermark = get_watermark(data, 0x331)
    if payload_type == 'HTTPS stager' and arch == 'x64' and payload_size > 0x38d:
        watermark = get_watermark(data, 0x38d)
    return watermark

### Raw parsers
# DNS parser
def parse_dns(data):
    dns_record_type = 0
    dns_query_options = 0
    dns_query_name = 'not found'
    output = ''

    dns_record_type = struct.unpack_from('<B', data, 0x12C)[0]
    dns_query_options = struct.unpack_from('<H', data, 0x127)[0]
    dns_query_name = get_str(data, 0x14b, 0x18a)

    if dns_record_type == 0x10:
        dns_record_type = '0x0010 | DNS_TYPE_TEXT'
    else:
        dns_record_type = '0x%04x (custom value)' % dns_record_type
    if dns_query_options == 0x248:
        dns_query_options = '0x0248 | DNS_QUERY_BYPASS_CACHE, DNS_QUERY_NO_HOSTS_FILE, DNS_QUERY_RETURN_MESSAGE'
    else:
        dns_query_options = '0x%04x (custom value)' % dns_query_options

    output = 'DNS query name:\t%s' % dns_query_name
    output += '\n%s\nDnsQuery_A API:\nRecord type:\t%s\nQuery options:\t%s\n%s\n' % (HR,dns_record_type,dns_query_options,HR)
    return output

# SMB parser
def parse_smb(data):
    smb_open_mode = 0
    smb_pipe_mode = 0
    smb_max_instances = 0
    smb_pipe_name = 'not found'
    output = ''

    smb_max_instances = struct.unpack_from('<B', data, 0xBD)[0]
    smb_pipe_mode = struct.unpack_from('<B', data, 0xBF)[0]
    smb_open_mode = struct.unpack_from('<B', data, 0xC1)[0]

    if smb_max_instances == 1:
        smb_max_instances = '0x%02x' % smb_max_instances
    else:
        smb_max_instances = '0x%02x  (custom value)' % smb_max_instances
    if smb_pipe_mode == 6:
        smb_pipe_mode = '0x%02x  | PIPE_TYPE_MESSAGE, PIPE_READMODE_MESSAGE' % smb_pipe_mode
    else:
        smb_pipe_mode = '0x%02x  (custom value)' % smb_pipe_mode
    if smb_open_mode == 3:
        smb_open_mode = '0x%02x  | PIPE_ACCESS_DUPLEX' % smb_open_mode
    else:
        smb_open_mode = '0x%02x  (custom value)' % smb_open_mode

    if len(data) > 0x15A:
        smb_pipe_name = get_str(data, 0x15a)

    output = 'Pipe name:\t%s' % smb_pipe_name
    output += '\n%s\nCreateNamedPipeA API:\nOpen mode:\t%s\nPipe mode:\t%s\nMax Instances:\t%s\n%s\n' % (HR,smb_open_mode,smb_pipe_mode,smb_max_instances,HR)
    return output

# TCP Bind / Reverse parser
def parse_tcp(data, arch):
    ip_offset = 0
    sin_offset = 0
    output = ''

    if arch == 'x86':
        ip_offset = 0xc5
        sin_offset = 0xca
    if arch == 'x64':
        ip_offset = 0xf2
        sin_offset = 0xee

    sin_addr = '%d.%d.%d.%d' % struct.unpack_from('BBBB', data, ip_offset)
    try:
        sin_family = SA_FAMILY_NAMES[struct.unpack_from('H', data, sin_offset)[0]]
    except KeyError:
        sin_family = 'UNKNOWN'
    sin_port = struct.unpack_from('>H', data, sin_offset+2)[0]

    output = 'SOCKADDR_IN structure:\nsin_addr:\t%s\nsin_port:\t%s\nsin_family:\t%s\n%s\n' % (sin_addr,sin_port,sin_family,HR)
    return output

# HTTP/HTTPS parser
def parse_http(data, arch, p_type):
    port_offset, rq_start, rq_end, rh_start, rh_end = 0,0,0,0,0
    request_query = 'not found'
    request_header = 'not found'
    request_addr = 'not found'
    output = ''
    request_type = ''

    if arch == 'x86' and p_type == 'HTTPS stager':
        payload_size = 0x331
        port_offset = 0xc4
        rq_start = 0x168
        rq_end = 0x1b8
        rh_start = 0x1b8
        rh_end = 0x2e8

    if arch == 'x64' and p_type == 'HTTPS stager':
        payload_size = 0x38d
        port_offset = 0x112
        rq_start = 0x1a9
        rq_end = 0x1f9
        rh_start = 0x1f9
        rh_end = 0x329

    if arch == 'x86' and p_type == 'HTTP stager':
        payload_size = 0x30c
        port_offset = 0xbf
        rq_start = 0x143
        rq_end = 0x193
        rh_start = 0x193
        rh_end = 0x2c3

    if arch == 'x64' and p_type == 'HTTP stager':
        payload_size = 0x36a
        port_offset = 0x10f
        rq_start = 0x186
        rq_end = 0x1d6
        rh_start = 0x1d6
        rh_end = 0x306

    request_port = struct.unpack_from('I', data, port_offset)[0]
    request_query = get_str(data, rq_start, rq_end)
    verify_query = checksum8(request_query)
    request_header = get_str(data, rh_start, rh_end)
    request_type = p_type[0:5].lower().strip()

    if len(data) > payload_size:
        request_addr = get_str(data, payload_size)

    output = 'Request detail:\nAddress:\t%s\nPort:\t\t%s\nQuery:\t\t%s (%s checksum)' % (request_addr, request_port, request_query, verify_query)
    output += '\n%s\nRequest header:' % HR
    for r_item in request_header.split('\r\n'):
        if r_item != '':
            output += '\n%s' % r_item
    output += '\n%s\n' % HR
    if request_addr != 'not found':
        output += create_curl_comand([verify_query, request_type, request_addr, request_port, request_query, request_header])

    return output

### Parse raw payload file
def raw_parser(p):
    report = ''
    try:
        with open(p,'rb') as f:
            buff = f.read()
    except OSError as e:
        print('%s\n[!] File:  %s\n[!] Error: %s\n%s' % (HR,p.name,e.strerror,HR))
        return False

    buff = fix_utf16(buff)
    payload_start_offset, payload_arch_type = get_payload_arch(buff)

    if not payload_arch_type or payload_start_offset == -1:
        print('%s\n[!] File:  %s\n[!] Error: Payload pattern not found.\n%s' % (HR,p.name,HR))
        return False

    data = buff[payload_start_offset:]
    payload_api_list = parse_api_functions(data, payload_arch_type)
    payload_type = get_payload_type(payload_api_list)

    if payload_type == 'unknown':
        print('%s\n[!] File:  %s\n[!] Error: Unknown payload type.\n%s' % (HR,p.name,HR))
        return False

    if not verify_payload_data(data, payload_type, payload_arch_type):
        print('%s\n[!] File:  %s\n[!] Error: Unknown payload type.\n%s' % (HR,p.name,HR))
        return False

    report = '%s\nFilename:\t%s\n%s\n' % (HR,p.name,HR)
    report += 'Architecture:\t%s\nPayload type:\t%s\nPayload start:\t0x%04x\n' % (payload_arch_type,payload_type,payload_start_offset)

    payload_watermark = parse_watermark(data,payload_type, payload_arch_type)

    if payload_watermark == 0:
        report += 'Customer ID:   \tnot found\n%s\n' % HR
    else:
        report += 'Customer ID:   \t0x%08x | %i\n%s\n' % (payload_watermark, payload_watermark,HR)

    if payload_type.startswith('DNS'):
        report += parse_dns(data)

    elif payload_type.startswith('SMB'):
        report += parse_smb(data)

    elif payload_type.startswith('TCP'):
        report += parse_tcp(data,payload_arch_type)

    elif payload_type.startswith('HTTP'):
        report += parse_http(data,payload_arch_type,payload_type)

    report += print_api_functions(payload_api_list, payload_start_offset)
    print(report)

    try:
        with open(p.with_name(p.name+'.log'),'w') as o:
           o.write(report)
    except OSError as e:
        print('%s\n[!] File: %s\n[!] Error: %s\n%s' % (HR,p.name,e.strerror,HR))
        return False

    return True

### Main
def main():
    print('%s\nCS Raw payload parser v%.02f%sAvast Software s.r.o' % (HR,VERSION,' '*33))
    if len(sys.argv) < 2:
        print('%s\n[!] Please specify input file or directory.' % HR)
        sys.exit()

    p = Path(sys.argv[1])
    # parse file
    if p.is_file():
        raw_parser(p)
    # parse files from directory
    elif p.is_dir():
        for fp in p.iterdir():
            if fp.is_file():
                raw_parser(fp)
    else:
        print('%s\n[!] Please specify input file or directory.' % HR)
        sys.exit()

if __name__ == "__main__":
    main()

