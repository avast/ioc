# IoC for Almaq

Malware analysis and more technical information at <https://decoded.avast.io/romanalinkeova/what's-new-in-this-year's-almanaq?/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [Network indicators](#network-indicators)

## Samples (SHA-256)
```
4098d92ead72b1b2749e2d58102327f670a1db2d46c6e74eefbbed7f68167265 - AlMashreqService.dll
9cbc09dd569942582a6ec3d94fb5c9fc70c1e43282dc36dcc8cdf8d0a5131235 - AlMashreqService.dll
8b4baa073900f9602845694f6d1f9358a196ea0b7dfc06ad320f9c162bff0141 - acrobat reader.exe
945426553022101b7a75c6b5cad3d780363193b5412ea077257873b1971dfed3 - adobe.exe
497c2e9aa686f12031df590c124e7a9d0f0b1df7bf52e5fbd9ffa1501e383e93 - Printer.exe
d61b743aa7e5b50f2ebe3f5a4cd31ee97d51282ba083b7dc5265888f5797ab88 - Printr.exe
6fef864850bf8a603305370dc5f522366af6392946a8049647d1423a9a62461c - spoolsv.exe
39f696883838d5ddc91f76fb8f1b547c20a9ef08e1f5e836bf64b7956e7644c3 - Service.exe
32f59e810ab96690c848097686a94c57de6221af6d299ac153f617b7c504bb55 - Service.exe
04e363bd90dea1b18d6f3f4f3f92b00ce55ee1289c05eb575a0f7cd0ab138902 - Dll.exe
2139f4084795ec07ec0ba78292154879c3bb1c495661471017a83355bf5f8af0 - DllLiberary.exe
07884b08b394f1cedec09e8e0bf46a7ef29d904e10cb0079893d294c7ab286a2 - svchost.exe
036760d3a1b4760e9bf5527f0fed0e0a8bb98b6dbec3d5de7d8aba6afbeaf82b - SearchFile.exe
081ea05b7476425189575ce5d30b941a61e252448cc8f8e5bc2a6c290d25d670 - security.exe
078cf6f436eb73112bf4dc00f601e4a82bd4476b55df660a1b19186c8b646fc1 - security.exe
```

## Network indicators
### C&C servers
```
http://servicesx.gearhostpreview[.]com/data.asmx
http://systemservicex.azurewebsites[.]net/data.asmx
http://adobereader.azurewebsites[.]net/data.asmx
http://gcmedservice.azurewebsites[.]net/Scripts.asmx
alhussienweb.ddns[.]net
```
### FTP servers
```
ftp://waws-prod-am2-253.ftp.azurewebsites.windows[.]net/site/wwwroot
ftp://waws-prod-sn1-071.ftp.azurewebsites.windows[.]net/site/wwwroot/
ftp://ftp.gear[.]host/site/wwwroot/
```