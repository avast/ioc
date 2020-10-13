# IoC for Meh

Malware analysis and more technical information at <https://decoded.avast.io/janrubin/complex-obfuscation-meh/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [File names](#file-names)
* [Network indicators](#network-indicators)


## Samples (SHA-256)
#### CoViper binary and related files
```
94c2479d0a222ebdce04c02f0b0e58ec433b62299c9a537a31090bb75a33a06e - Initial AutoIt script
43bfa7e8b83b54b18b6b48365008b2588a15ccebb3db57b2b9311f257e81f34c - Stage 1 - Dropper
34684e4c46d237bfd8964d3bb1fae8a7d04faa6562d8a41d0523796f2e80a2a6 - Stage 2 - Shellcode
2256801ef5bfe8743c548a580fefe6822c87b1d3105ffb593cbaef0f806344c5 - Stage 3 - Shellcode 2
657ea4bf4e591d48ee4aaa2233e870eb99a17435968652e31fc9f33bbb2fe282 - Stage 4 - Meh stager
66de6f71f268a76358f88dc882fad2d2eaaec273b4d946ed930b8b7571f778a8 - pe.bin
75949175f00eb365a94266b5da285ec3f6c46dadfd8db48ef0d3c4f079ac6d30 - base.au3
1da298cab4d537b0b7b5dabf09bff6a212b9e45731e0cc772f99026005fb9e48 - autoit.exe


```

## File names
```
C:\testintel2\pe.bin
C:\testintel2\base.au3
C:\testintel2\autoit.exe
C:\testintel2\a.txt
C:\programdata\intel\wireless
```

## Network indicators
#### Downloader urls
```
http://83[.]171.237.233/s2/pe.bin
http://83[.]171.237.233/s2/base.au3
http://83[.]171.237.233/s2/autoit.exe
```
#### C&C servers
```
http://83[.]171.237.233
```
