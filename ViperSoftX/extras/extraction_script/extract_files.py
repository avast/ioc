from mainfest_pb2 import Mainfest
from malduck import aes, sha256, uint32
from pathlib import Path
import argparse


def decrypt(data: bytes) -> bytes:
	key = bytes.fromhex("71C54C3BCFFCE591A70C0B5BA6448327BC975D89F3021053125F1CB9A7C0AF72")
	iv = bytes.fromhex("C0BA0B56EAC742AFD4CB680EE0EB4FB0")

	decrypted = aes.cbc.decrypt(key, iv, data)
	pad_len = decrypted[-1]
	padding = decrypted[-pad_len:]
	assert all(x == pad_len for x in padding)
	return decrypted[:-pad_len]


def load_manifest(data: bytes) -> Mainfest:  # The "typo" is intetional
	manifest = Mainfest()
	decrypted_data = decrypt(data)
	manifest.ParseFromString(decrypted_data)
	return manifest


def find_encrypted_manifest(data: bytes) -> bytes:
	test_data = data[-0x24: -0x20]
	checksum = data[-0x20:]
	print(test_data, checksum)
	assert sha256(test_data) == checksum
	offset = uint32(test_data)
	assert isinstance(offset, int)
	return data[-0x24 - offset: -0x24]


def extract_files(manifest: Mainfest, data: bytes):
	outdir = Path("extracted_files")
	outdir.mkdir(exist_ok=True)

	(outdir/"manifest.dat").write_bytes(manifest.SerializeToString())

	for i, f in enumerate(manifest.Files):
		print(f)
		content = data[f.Offset: f.Offset + f.Size]
		outf = outdir / str(i)
		outf.write_bytes(decrypt(content))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog = 'Extractor for ViperSoftX\'s initial payloads (commonly named Activator.exe)',
		description = "This script extracts files from ViperSoftX\'s initial payloads (commonly named Activator.exe)")
	parser.add_argument('filepath')
	args = parser.parse_args()

	path = Path(args.filepath)
	if not Path.exists(path) or not Path.is_file(path):
		print("[!] The provided path does not exist or is not a file!")
		exit(1)

	data = b""
	with open(path, "rb") as fd:
		data = fd.read()

	enc_manifest = find_encrypted_manifest(data)  # find offset
	manifest = load_manifest(enc_manifest)  # decrypt and load protobuf
	extract_files(manifest, data)  # dump manifest and extracted files
