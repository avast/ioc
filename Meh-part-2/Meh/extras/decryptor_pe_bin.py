import os
import base64
import sys

if len(sys.argv) != 2:
    print("[!] Wrong number of parameters! A path to the pe.bin file expected.")
    exit(1)

path = sys.argv[1]
if not os.path.exists(path):
    print("[!] The file path provided does not exist!")
    exit(1)

file_contents = ''
with open(path, "r") as f:
    file_contents = f.read()

# Parse the base64 and obtain the xor key
parsed = file_contents.split('|')
if len(parsed) < 3:
    print("Provided file does not have the correct format.")
    exit(1)

xor_key = bytearray(parsed[1][:-1], "utf-8")
xor_key[0] = 0x61  # 'a'

file_contents_pe = parsed[2]

# Decode base64 content
file_contents_pe = base64.b64decode(file_contents_pe)

# Derive the one byte key
key = len(xor_key)
for i in range(0, len(xor_key)):
     key = xor_key[i] ^ key

result = b''
key = key ^ 255
for i in range(0, len(file_contents_pe)):
    result += bytes([file_contents_pe[i] ^ key])

with open("decrypted_pe_bin.dat", "bw") as f:
    f.write(result)

exit(0)
