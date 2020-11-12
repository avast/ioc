__author__ = "Jan Rubin, Avast Software"

from base64 import b64decode
from functools import reduce
from typing import Optional


def decrypt(encoded_text: bytes, key_material: bytes) -> bytes:
    ciphertext = b64decode(encoded_text)
    key = reduce(lambda x, y: x ^ y, key_material)  # XOR all bytes of the key
    key ^= len(key_material)
    
    plaintext = bytes([key ^ 255 ^ byte for byte in ciphertext])
    return plaintext


def find_key(offset: int) -> Optional[bytes]:
    for i in range(32):  # scan next 32 bytes for the decryption function
        offset += 1
        if print_operand(offset, 0) != "sub_448F58":
            continue
        
        string_offset = get_operand_value(offset - 0x5, 1)
        string = get_strlit_contents(string_offset)
        
        return string


def process_string(offset: int, ciphertext: bytes, key_material: bytes) -> int:
    decrypted = decrypt(ciphertext, key_material)
    try:
        set_cmt(offset, str(decrypted), False)
        return 1
    except Exception as error:
        print(f"[!] Could not resolve address {offset}, error: {error}")
        return 0


def find_strings(base: int, end: int):
    ea = base
    count = 0
    while ea <= end:
        ea = idc.next_addr(ea)
        if not print_operand(ea, 0) == "sub_443DDC":
            continue
        
        addr_key = get_operand_value(ea - 0x5, 1)
        ciphertext = get_strlit_contents(addr_key)
        key_material = find_key(ea)

        if key_material == None or ciphertext == None:
            ea = idc.next_addr(ea)
            continue

        count += process_string(ea, ciphertext, key_material)

    if count > 0:
        print(f"[+] Successfully decrypted {count} strings")
    else:
        print("[-] Could not decrypt strings. See errors above.")


print("Start decrypt")
find_strings(base=0x00401000, end=0x0044f000)