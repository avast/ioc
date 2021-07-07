from itertools import product
import string
import sys

# checksum8 algo
def checksum8(s):
    checksum = 0
    if s.startswith('/'):
        s = s[1:]
    if len(s) >= 4:
        checksum = sum([ord(ch) for ch in s]) % 0x100
    return checksum

# generate and verify request query strings
def generate_list(rep=4):
    chars = string.ascii_letters + string.digits
    to_attempt = product(chars, repeat=rep)
    for attempt in to_attempt:
        word = ''.join(attempt)
        if checksum8(word) == 92:
            print('/%s, x86 checksum' % word)
        if checksum8(word) == 93:
            print('/%s, x64 checksum' % word)

# verify string
def verify_checksum(s):
    if checksum8(s) == 92:
        print('%s is valid x86 checksum' % s)
    elif checksum8(s) == 93:
        print('%s is valid x64 checksum' % s)
    else:
        print('%s is not valid checksum' % s)

def main():
    if len(sys.argv) < 3:
        print('Usage:\nGenerate word list:\nchecksum8.py -g <string_size>\nVerify string:\nchecksum8.py -v <string>')
        sys.exit()

    if sys.argv[1] == '-g':
        try:
            string_size = int(sys.argv[2])
            generate_list(string_size)
        except ValueError:
            print('Wrong input format.\nPlease input valid number.\nExample: checksum8.py -g 4')
            sys.exit()

    elif sys.argv[1] == '-v':
        verify_checksum(sys.argv[2])

    else:
        print('Usage:\nGenerate word list:\nchecksum8.py -g <string_size>\nVerify string:\nchecksum8.py -v <string>')
        sys.exit()

if __name__ == "__main__":
    main()