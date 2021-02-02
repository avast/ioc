import base64
import sys

def strrevsstr(ciphertext: str) -> str:
	if len(ciphertext) % 4 != 0:
		ciphertext = ciphertext + (4 - (len(ciphertext) % 4)) * '='
	ciphertext = ciphertext.replace('-', '+').replace('_', '/')
	ciphertext = base64.b64decode(ciphertext)

	f = int(ciphertext[0:2], 16)
	f2 = int(ciphertext[2:3], 16)

	for i in range (3, len(ciphertext)):
		if ciphertext[i] < ord('0') or ciphertext[i] > ord('9'):
			first_non_digit_index = i
			break

	length = int(ciphertext[3:first_non_digit_index])
	ciphertext = ciphertext[first_non_digit_index+1:]

	if length != len(ciphertext):
		print("[.] Warning: length mismatch %d != %d" % (length, len(ciphertext)))
		print("[.] Possibly truncated ciphertext")

	e = f
	plaintext = ""
	for i, c in enumerate(ciphertext):
		b = c ^ e
		if i > f2:
			b ^= ciphertext[i - f2]
		e = c ^ f
		plaintext += chr(b)

	return plaintext



if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("[!] Wrong number of parameters. Expected ciphertext.")
		exit(1)

	ct = sys.argv[1]

	print(strrevsstr(ct))