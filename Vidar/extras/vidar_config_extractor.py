# MIT License
#
# Copyright (c) 2026 Gen Digital Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Static Vidar config extractor (XOR variant).

Tested with:
    296C97D66AC4CB05777F053FA2C17E78B415567E449D169AA3CF683A6565D28A (Vidar version 1.5)
    16911BD74F0D6751A30A1BE56A3752DAF7BF333C0D6EC61D8746646DBE2A530D (Vidar version 1.6)
    27D4AD97468FA0388BC704A32DD5C5E21E6B1DE76A160FBD2615530C58AA74A6 (Vidar version 1.7)
    155F9F56FCDAB7DD03740656EAA27000AD68F76A4F7B4933FA57416278E909A7 (Vidar version 1.8)

Blob layout (offsets from blob start):
    +0x000  key[16]            XOR key
    +0x010  version            len @ +0x030
    +0x031  build_id           len @ +0x071
    +0x072  C2 record[k]:
                +0x000  url         len @ +0x100
                +0x101  tag         len @ +0x141
                +0x142  user_agent  len @ +0x242
"""

import argparse
import itertools
import json
import os
import re
import sys

import numpy as np


KEYLEN = 16
VER_OFF = 0x010          # version ciphertext
VER_LEN = 0x030          # version length byte
BID_OFF = 0x031          # build_id ciphertext
BID_LEN = 0x071          # build_id length byte
RECS    = 0x072          # first C2 record
URL_OFF = 0x000          # url ciphertext
URL_LEN = 0x100          # url length byte
TAG_OFF = 0x101          # tag ciphertext
TAG_LEN = 0x141          # tag length byte
UA_OFF  = 0x142          # user_agent ciphertext
UA_LEN  = 0x242          # user_agent length byte
REC_STRIDE = 0x243       # UA_LEN + 1
MAX_RECORDS = 32
MAX_FILE_SIZE = 64 * 1024 * 1024

VER_RE = re.compile(rb"^[0-9]{1,3}(?:\.[0-9]{1,3}){1,3}$")


def _decrypt(buf: bytes, base: int, ct_off: int, len_off: int, key: bytes) -> bytes | None:
    if base + len_off >= len(buf):
        return None
    n = buf[base + len_off]
    if n == 0:
        return b""
    if base + ct_off + n > len(buf):
        return None
    ct = buf[base + ct_off : base + ct_off + n]
    return bytes(a ^ b for a, b in zip(ct, itertools.cycle(key)))


def _is_printable(b: bytes) -> bool:
    return len(b) > 0 and all(0x20 <= c <= 0x7E for c in b)


def _try_blob(buf: bytes, off: int) -> dict | None:
    if off + RECS + REC_STRIDE > len(buf):
        return None
    if not 3 <= buf[off + VER_LEN] <= 15:
        return None

    key = buf[off : off + KEYLEN]
    version = _decrypt(buf, off, VER_OFF, VER_LEN, key)
    if not version or not VER_RE.match(version):
        return None

    url0 = _decrypt(buf, off + RECS, URL_OFF, URL_LEN, key)
    if not url0 or not url0.startswith(b"http"):
        return None

    build_id = _decrypt(buf, off, BID_OFF, BID_LEN, key) or b""
    if build_id and not _is_printable(build_id):
        return None

    records = []
    for k in range(MAX_RECORDS):
        rb = off + RECS + REC_STRIDE * k
        url = _decrypt(buf, rb, URL_OFF, URL_LEN, key)
        if not url or not url.startswith(b"http") or not _is_printable(url):
            break
        records.append({
            "url":        url.decode("latin1"),
            "tag":        (_decrypt(buf, rb, TAG_OFF, TAG_LEN, key) or b"").decode("latin1"),
            "user_agent": (_decrypt(buf, rb, UA_OFF,  UA_LEN,  key) or b"").decode("latin1"),
        })

    return {
        "version": version.decode("latin1"),
        "build_id": build_id.decode("latin1"),
        "c2": records,
    }


def extract(data: bytes) -> dict | None:
    hi = len(data) - (RECS + REC_STRIDE)
    if hi <= RECS + 4:
        return None
    a = np.frombuffer(data, dtype=np.uint8)
    mask = np.ones(hi, dtype=bool)
    for i, ch in enumerate(b"http"):
        mask &= (a[RECS + i : RECS + i + hi] ^ a[i : i + hi]) == ch
    for off in np.nonzero(mask)[0]:
        cfg = _try_blob(data, int(off))
        if cfg:
            return cfg
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Vidar XOR config extractor")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", help="single sample file")
    group.add_argument("-d", help="directory of samples")
    args = parser.parse_args()

    targets: list[str] = []
    if args.s:
        targets.append(args.s)
    elif args.d:
        try:
            for f in sorted(os.listdir(args.d)):
                path = os.path.join(args.d, f)
                if os.path.isfile(path):
                    targets.append(path)
        except OSError as e:
            print(f"Error reading directory: {e}")
            sys.exit(1)

    for target in targets:
        try:
            with open(target, "rb") as f:
                data = f.read(MAX_FILE_SIZE)
            cfg = extract(data)
            if cfg:
                print(f"\033[92m[Extracted configuration]: {os.path.basename(target)}\033[0m")
                print(json.dumps(cfg, indent=4))
            else:
                print(f"\033[91m[Extraction failed]: {os.path.basename(target)}\033[0m")
        except OSError as e:
            print(f"\033[91mError opening file: {os.path.basename(target)}: {e}\033[0m")


if __name__ == "__main__":
    main()
