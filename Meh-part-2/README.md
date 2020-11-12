# IoC for Meh part 2

Malware analysis and more technical information at <https://decoded.avast.io/janrubin/meh-2-2/>

The technical analysis of the first part of the blogpost series can be found at <https://decoded.avast.io/janrubin/complex-obfuscation-meh/>
IoCs of the first part of the blogpost series can be found at <https://github.com/avast/ioc/tree/master/Meh>

### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [File names](#file-names)
* [Network indicators](#network-indicators)


## Samples (SHA-256)
#### Meh binary and related files
```
94c2479d0a222ebdce04c02f0b0e58ec433b62299c9a537a31090bb75a33a06e - Initial AutoIt script
43bfa7e8b83b54b18b6b48365008b2588a15ccebb3db57b2b9311f257e81f34c - Stage 1 - Dropper
34684e4c46d237bfd8964d3bb1fae8a7d04faa6562d8a41d0523796f2e80a2a6 - Stage 2 - Shellcode
2256801ef5bfe8743c548a580fefe6822c87b1d3105ffb593cbaef0f806344c5 - Stage 3 - Shellcode 2
657ea4bf4e591d48ee4aaa2233e870eb99a17435968652e31fc9f33bbb2fe282 - Stage 4 - Meh stager
66de6f71f268a76358f88dc882fad2d2eaaec273b4d946ed930b8b7571f778a8 - pe.bin
75949175f00eb365a94266b5da285ec3f6c46dadfd8db48ef0d3c4f079ac6d30 - base.au3
1da298cab4d537b0b7b5dabf09bff6a212b9e45731e0cc772f99026005fb9e48 - autoit.exe
1f13024724491b4b083dfead60931dcacabd70e5bd674c41a83a02410dea070d - Meh password stealer
3c1e5930d35815097435268fab724a6ed1bc347dd97cd20eb05f645a25eb692b - cpux64.bin
57b6fa7cbc98b752da6002e1b877a0e1d83f453f9227044b0b96bf28b0131195 - cpux86.bin
722502b7302fd6bae93c57212fcafad2767c5f869e37bd00487b946f76251c8d - cpux64.bin unpacked
e96403de3807ccb740f9ca6cade9ebd85696485590f51a4eb1c308de9875dfaa - cpux86.bin unpacked
```

## File names
```
C:\ProgramData\Intel\Wireless\
C:\Users\<user>\AppData\Local\Temp\test.txt
C:\Users\<user>\AppData\Local\Temp\torrent.txt
```

## Network indicators
#### C&C servers
```
http[:]//193-22-92-35.intesre.com
http[:]//0.le4net00.net
http[:]//83.171.237.231
http[:]//deploy.static.blazingtechnologies.io
http[:]//0.weathdata.nu
http[:]//124.red-79-152-243.dynamicip.fina-tdl.io
```
