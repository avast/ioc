# Payload tools

Python scripts for extracting and parsing x86 and x64 payloads.

## cs_payload_parser.py
Parser support DNS, SMB, TCP Bind/Reverse, HTTP/HTTPS payloads.

Usage:
```
cs_payload_parser.py <file_or_directory>
```
Example:
```
cs_payload_parser.py memdump.bin
cs_payload_parser.py c:\cs_payloads\
```

## cs_payload_extractor.py

Payload extractor and parser for various encoded formats (hex, hex_array, hex_veil, dec_array, chr_array, base64, xor, inflate, gzip).

Usage:
```
cs_payload_extractor.py <file_or_directory>
```
Example:
```
cs_payload_extractor.py memdump.bin
cs_payload_extractor.py c:\cs_payloads\
```