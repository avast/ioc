import re
import zlib
import binascii
import base64
import struct
import sys
from pathlib import Path
import cs_payload_parser as csp

### Constants
VERSION = 1.0
# Regex patterns for default CS encoding
FILE_TYPE_PATTERNS = [
    ['raw_payload', b'\xFC\xE8\x89\x00\x00\x00\x60\x89|\xFC\x48\x83\xE4\xF0\xE8\xC8\x00'],
    ['xored_payload', b'\x10[\x00-\xFF]{1}\x00\x00[\x00-\xFF]{3}\x00[\x00-\xFF]{4}\x61\x61\x61\x61'],
    ['xored_beacon', b'\xFC\xE8.\x00\x00\x00.{,32}\xEB[\x27\x2B].\x8B.\x00?\x83.\x04\x55?\x8B.\x00?\x31.\x83.\x04|\xFC\x48\x83\xE4\xF0\xEB\x33\x5D\x8B\x45\x00\x48\x83\xC5\x04\x8B\x4D\x00\x31\xC1\x48'],
    ['raw_hex', b'[a-fA-F0-9]{255,}'],
    ['raw_hex_array', b'(0x[a-fA-F0-9]{2}([;,\.]\s)?){255,}'],
    ['raw_hex_veil', rb'(\\x[a-fA-F0-9]{2}){255,}'],
    ['raw_dec_array',rb'([0-9\-]{1,4},(\s_\n)?[0-9\-]{1,4},?){255,}'],
    ['raw_chr_array', b'([aArR"&y\s]{5,})?(Chr\([0-9\-]{1,4}\)&("[a-zA-Z0-9\s]{1,}"&)?(\s_\n)?){32,}'],
    ['raw_base64', b'(?:[A-Za-z0-9+/]{4}){128,}(?:[A-Za-z0-9+/][AQgw]==|[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=)?']
]
# Default XOR key used in encoding postprocess
DEFAULT_CS_XOR_KEY = 0x23
# decorations
HR = '-'*80

### Helper functions
# Check regex pattern
def check_pattern(patterns, buff):
    data = ('unknown', b'')
    for pattern in patterns:
        r = re.compile(pattern[1], re.IGNORECASE)
        m = re.search(r,buff)
        if m:
            data = (pattern[0],m.group())
            return data
    return data

# Return dword value from offset
def dword(buff, p_offset):
    return  struct.unpack_from('<I',buff, p_offset)[0]

# Convert matched object to byte
def convert_to_byte(m):
    if m.group(1) is not None:
        return struct.pack('b', int(m.group(1)))

# Remove utf-16-le encoding
def fix_utf16(buff):
    r = re.compile(b'^([\x00-\xff]\x00){200,}')
    m = re.search(r,buff)
    if m:
        buff = re.sub(b'([\x00-\xff])\x00', rb'\1', buff)
    return buff

### Post process functions
# One byte xor
def xor(buff, key=DEFAULT_CS_XOR_KEY):
    return bytes([b ^ key for b in buff])

# Inflate without headers
def inflate(buff):
    data = zlib.decompressobj(wbits=-15) # -15 = no headers and trailers
    decompressed_data = data.decompress(buff)
    decompressed_data += data.flush()
    return decompressed_data

# Gzip unpack
def gunzip(buff):
    data = zlib.decompressobj(wbits=47) # 47 = zlib + gzip headers and trailers
    decompressed_data = data.decompress(buff)
    decompressed_data += data.flush()
    return decompressed_data

# Post process
def post_process(data,buff):
    r = re.compile(b'Compression\.GzipStream', re.IGNORECASE)
    m = re.search(r, buff)
    if m:
        data = gunzip(data)
    r = re.compile(b'Compression\.DeflateStream', re.IGNORECASE)
    m = re.search(r, buff)
    if m:
        data = inflate(data)
    r = re.compile(b'-bxor (\d{1,3})')
    m = re.search(r, buff)
    if m:
        xor_key = int(m.group(1))
        data = xor(data,xor_key)
    return data


### Extractor functions
# Raw hex format
# Usage: VBS, HTA scripts
# Example: 4d5a9000..
def raw_hex(data):
    return binascii.unhexlify(data)

# Hex array
# Usage: PS1 scripts
# Example: 0x4d, 0x5a, 0x90, 0x00...
def raw_hex_array(data):
    data = re.sub(b'0x|[;,\.\s]', b'', data)
    return binascii.unhexlify(data)

# Hex veil
# Usage: PY scripts
# Example: \x4d\x5a\x90\x00..
def raw_hex_veil(data):
    data = re.sub(rb'\\x', b'', data)
    return binascii.unhexlify(data)

# Decimal array
# Usage: VBA scripts
# Example: -4,-24,-119,0,0..
def raw_dec_array(data):
    output = b''
    data = re.sub(b'[_\n\s]', b'', data)
    for n in data.split(b','):
        output += struct.pack('b',int(n))
    return output

# Char array
# Usage: VBS, HTA scripts
# Example: Chr(-4)&"H"&Chr(-125)&Chr(-28)..
def raw_chr_array(data):
    output = b''
    data = data.replace(b'\n', b'')
    data = re.sub(b'\s_',b'', data)
    data = re.sub(b'["&]',b'',data)
    dec = re.sub(b'Chr\((-?\d{1,3})\)', convert_to_byte, data)
    output = dec
    if not dec.startswith(b'\xFC'):
        dec = dec.replace(b'\n', b'')
        r = re.compile(b'[aArRyY]{5}\(([0-9\-,_]+)\)')
        m = re.search(r, dec)
        if m:
            output = raw_dec_array(m.group(1))
    return output

# Base64 blob
# Usage: PS1 scripts
# Example: 38uqIyMjQ6..
def raw_base64(data):
    output = b''
    output = base64.b64decode(data)
    if output.startswith((b'\xfc\x00',b'\x4d\x00',b'\x90\x00')):
        output = re.sub(b'([\x00-\xff])\x00', rb'\1', output)
    return output

# Xored beacon format
# Usage: downloaded beacons
def xored_beacon(buff):
    enc_offset = 0
    start_offset = 0
    dexored_buff = b''
    r = re.compile(b'(\xFC\xE8.\x00\x00\x00|\xFC\x48\x83\xE4\xF0\xEB)')
    s = re.search(r,buff)
    r = re.compile(b'\xFF.\xE8.\xFF\xFF\xFF')
    m = re.search(r,buff)
    if not m or not s:
        print('[!] Decrypt loop not found..')
        return dexored_buff
    enc_offset = m.start()+7
    start_offset = s.start()
    if enc_offset > 32 and 0x10 <= enc_offset-start_offset <= 0x100:
        init_key = dword(buff, enc_offset)
        size = dword(buff, enc_offset+4) ^ init_key
        if enc_offset+size > len(buff) or size % 4 !=0:
            print('[!] Payload size is wrong..')
            return dexored_buff
        # Xor with rolling dword key
        enc_offset += 8
        for i in range(0,size,4):
            enc_dw = dword(buff, enc_offset+i)
            dec = enc_dw ^ init_key
            dexored_buff += struct.pack("<I",dec)
            init_key = init_key ^ dec
        return dexored_buff
    print('[!] Invalid decrypt loop..')
    return dexored_buff

# Xored payload
# Usage: PE stagers/stageless binaries
def find_xored_payload_header(buff):
    r = re.compile(b'\x10[\x00-\xFF]{1}\x00\x00[\x00-\xFF]{3}\x00[\x00-\xFF]{4}\x61\x61\x61\x61')
    m = re.search(r,buff)
    if m:
        return m.start()
    else:
        return -1
# Xor with dword key
def xored_payload(buff):
    dexored_buff = b''
    header_offset = find_xored_payload_header(buff)
    if header_offset >= 0:
        p_offset,p_size,p_xor_key,p_junk = struct.unpack_from('<IIII', buff, header_offset)
        enc_buff = buff[p_offset:p_offset+p_size]
        if len(enc_buff) == p_size:
            p_xor_key = p_xor_key.to_bytes(4,'little')
            for i in range(len(enc_buff)):
                dexored_buff += struct.pack("<B",enc_buff[i]^p_xor_key[i%4])
    return dexored_buff

# Raw CS payload
# Usage: Encoded scripts, PE binaries
def find_raw_payload_header(buff):
    r = re.compile(b'(\xFC\xE8\x89\x00\x00\x00\x60\x89|\xFC\x48\x83\xE4\xF0\xE8\xC8\x00)')
    m = re.search(r,buff)
    if m:
        return m.start()
    else:
        return -1
# Return raw buffer payload data
def raw_payload(buff):
    dexored_buff = b''
    header_offset = find_raw_payload_header(buff)
    if header_offset >= 0:
        dexored_buff = buff[header_offset:header_offset+4096]
    return dexored_buff

### Extract payloads from encoded or binary files
def extract_payload(p):
    decoded_buff = b''
    output_path = ''
    try:
        with open(p,'rb') as f:
            buff = f.read()
    except OSError as e:
        print('%s\n[!] File:  %s\n[!] Error: %s\n%s' % (HR,p.name,e.strerror,HR))
        return False

    buff = fix_utf16(buff)
    ft, enc = check_pattern(FILE_TYPE_PATTERNS,buff)

    if ft in ['raw_hex', 'raw_hex_array', 'raw_hex_veil', 'raw_dec_array','raw_base64']:
        decoded_buff = globals()[ft](enc)
    elif ft in ['raw_chr_array', 'xored_payload', 'raw_payload', 'xored_beacon']:
        decoded_buff = globals()[ft](buff)
    else:
        print('%s\n[!] File:  %s\n[!] Error: Payload pattern not found.\n%s' % (HR,p.name,HR))
        return False

    print('%s\nFilename:\t%s\nPayload type:\t%s\n%s' % (HR,p.name,ft,HR))
    decoded_buff = post_process(decoded_buff,buff)

    if len(decoded_buff) == 0:
        print('[!] Error: Extracting payload fails.\n%s' % HR)
        return False

    output_path = p.with_name(p.name+'_payload.bin')

    try:
        with open(output_path,'wb') as o:
           o.write(decoded_buff)
           print('Saved as:\t%s\n%s' % (p.name+'_payload.bin',HR))
    except OSError as e:
        print('%s\n[!] File: %s\n[!] Error: %s\n%s' % (HR,p.name,e.strerror,HR))
        return False

    return True, ft, output_path

### Main
def main():
    print('%s\nCS Payload extractor v%.02f%sAvast Software s.r.o\n%s' % (HR,VERSION,' '*34,HR))
    if len(sys.argv) < 2:
        print('%s\n[!] Please specify input file or directory.' % HR)
        sys.exit()

    p = Path(sys.argv[1])
    # extract and parse file
    if p.is_file():
        print('[*] Extracting file..')
        d = extract_payload(p)
        if d:
            print('[*] Parsing file..')
            csp.raw_parser(d[2])
    # extract and parse files from directory
    elif p.is_dir():
        for fp in p.iterdir():
            if fp.is_file():
                print('\n%s\n[*] Extracting file..' % HR)
                d = extract_payload(fp)
                if d:
                    print('[*] Parsing file..')
                    csp.raw_parser(d[2])
    else:
        print('%s\n[!] Please specify input file or directory.' % HR)
        sys.exit()

if __name__ == "__main__":
    main()
