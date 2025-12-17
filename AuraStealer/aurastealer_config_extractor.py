import sys, json, os, argparse
from typing import Optional
from Cryptodome.Cipher import AES


def extract(data: bytes) -> bytes:
    """
    Encrypted config structure:
        [AES_KEY]              - 32 bytes
        [AES_IV]               - 16 bytes
        [LEN_MASKED]           - 4 bytes (data length XORed with MASK
        [MASK]                 - 4 bytes
        [ENCRYPTED_DATA]       - LEN bytes (AES-CBC encrypted config data with PKCS#7 padding)
    """
    # The config is typically of size < 500 bytes, so 2kB chunks should be enough
    CHUNK_SIZE = 2048
    for addr in range(0, len(data) - CHUNK_SIZE + 1, 4):
        chunk = data[addr : addr + CHUNK_SIZE]

        aes_key = chunk[:32]
        aes_iv = chunk[32:48]
        data_len_masked = int.from_bytes(chunk[48:52], "little")
        mask = int.from_bytes(chunk[52:56], "little")
        data_len = data_len_masked ^ mask

        if data_len + 56 <= len(chunk) and data_len > 0:
            encrypted = chunk[56 : 56 + data_len]
            try:
                decrypted = AES.new(aes_key, AES.MODE_CBC, aes_iv).decrypt(encrypted)
            except (ValueError, TypeError):
                continue

            # Remove PKCS#7 padding
            decrypted = decrypted.rstrip(bytes([decrypted[-1]])).rstrip(b"\x00")

            # Check all bytes are printable ASCII
            if all(32 <= b <= 127 for b in decrypted):
                return decrypted
    return None


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", help="sample file")
    group.add_argument("-d", help="directory of samples")
    args = parser.parse_args()

    targets = []
    if args.s:
        targets.append(args.s)
    elif args.d:
        try:
            for f in os.listdir(args.d):
                path = os.path.join(args.d, f)
                if os.path.isfile(path):
                    targets.append(path)
        except OSError as e:
            print(f"Error reading directory: {e}")
            sys.exit(1)

    for target in targets:
        try:
            with open(target, "rb") as f:
                data = f.read()
                decrypted_raw = extract(data)
                if decrypted_raw:
                    print(
                        f"\033[92m[Extracted configuration]: {os.path.basename(target)}\033[0m"
                    )
                    try:
                        obj = json.loads(decrypted_raw)
                        print(f"{json.dumps(obj, indent=4)}")
                    except json.JSONDecodeError:
                        print(f"{decrypted_raw.decode('utf-8')}")
                else:
                    print(
                        f"\033[91m[Extraction failed]: {os.path.basename(target)}\033[0m"
                    )
        except IOError:
            print(f"\033[91mError opening file: {os.path.basename(target)}\033[0m")


if __name__ == "__main__":
    main()
