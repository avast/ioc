import sys
import pefile
from pathlib import Path

def ROR(data, bits):
    return (data >> bits | data << (32 - bits)) & 0xFFFFFFFF

def hash_api(dll_name, api_name):
    # normalize api name
    api = bytes(api_name,'utf-8') + b'\x00'
    # normalize dll name
    dll = dll_name.upper().encode('utf-16')[2:] + b'\x00\x00'
    # compute api hash
    api_hash = 0
    for i in range(len(api)):
        api_hash = ROR(api_hash,0x0d) + api[i]
    # compute dll hash
    dll_hash = 0
    for i in range(len(dll)):
        dll_hash = ROR(dll_hash,0x0d) + dll[i]
    # compute final hash
    final_hash = (api_hash + dll_hash) & 0xFFFFFFFF
    print('0x%08x,%s_%s' % (final_hash, dll_name, api_name))

def compute_dir(p,file_type='dll'):
    for fp in p.iterdir():
        if fp.is_file() and fp.name.endswith(file_type):
            pe = pefile.PE(fp)
            try:
                for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                    if export.name != None:
                        hash_api(fp.name, export.name.decode('utf-8'))
            except:
                pass

def main():
    if len(sys.argv) < 3:
        print('Usage:\ngenerate_hash.py -i <dll_name,api_name>\ngenerate_hash.py -d <path_to_directory>')
        sys.exit()

    if sys.argv[1] == '-i':
        try:
            dll_name,api_name = sys.argv[2].split(',')
            hash_api(dll_name,api_name)
        except ValueError:
            print('Wrong input format.\nPlease use: dll_name,api_name\nExample: generate_hash.py -i kernel32.dll,VirtualAlloc')
            sys.exit()

    elif sys.argv[1] == '-d':
        p = Path(sys.argv[2])
        if p.is_dir():
            compute_dir(p)
        else:
            print('Wrong path. Please input valid path to directory.')
            sys.exit()

    else:
        print('Usage:\ngenerate_hash.py -i <dll_name,api_name>\ngenerate_hash.py -d <path_to_directory>')
        sys.exit()

if __name__ == "__main__":
    main()
