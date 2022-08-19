import re
import zlib
import binascii
import sys

def inflate(buff):
    data = zlib.decompressobj(wbits=-15) # -15 = no headers and trailers
    try:
        decompressed_data = data.decompress(buff)
        decompressed_data += data.flush()
        return decompressed_data
    except:
        print('Inflate error..')
        sys.exit()

def raw_hex(data):
    try:
        return binascii.unhexlify(data)
    except:
        print('Hexstring data error..')
        sys.exit()

def decode_payload(buff):
    payload_type = 'ELF'
    decoded = inflate(raw_hex(buff))
    if decoded.startswith(b'MZ'):
        payload_type = 'EXE'
    o_name = 'payload_' + payload_type + '_decoded.bin'
    o = open(o_name,'wb')
    o.write(decoded)
    o.close()
    print(o_name+ ' saved.')


def main():
    if len(sys.argv) < 2:
        print('usage: rip.py path_to_framework_file')
        sys.exit()
    try:
        f = open(sys.argv[1],'rb')
    except Exception as e:
        print(e)
        sys.exit()
    else:
        buff = f.read()
        f.close()

    r =  re.compile(b'1f8b08000000000000ff[0-9a-f]{1024,}?')
    items = re.finditer(r, buff)
    payloads = list(items)[-2:]

    if len(payloads) < 2:
        print('Payloads not found..')
        sys.exit()

    payload_1_start = payloads[0].start()
    payload_1_end = payloads[1].start()
    payload_1_buff = buff[payload_1_start+20:payload_1_end]
    decode_payload(payload_1_buff)

    payload_2_start = payload_1_end
    payload_2_end = re.search(b'[0-9a-f]{4}?\x00', buff[payload_2_start:]).start() + 4 + payload_2_start
    payload_2_buff = buff[payload_2_start+20:payload_2_end]
    decode_payload(payload_2_buff)

if __name__ == "__main__":
    main()
