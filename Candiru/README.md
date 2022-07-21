# IoC for Candiru

Analysis and more technical information at <https://decoded.avast.io/janvojtesek/the-return-of-candiru-zero-days-in-the-middle-east/>

### Table of Contents
* [Network indicators](#network-indicators)
* [Filesystem indicators](#filesystem-indicators)
* [Hijacked CLSIDs](#hijacked-clsids)


## Network indicators
```
bad-shop[.]net
bestcarent[.]org
core-update[.]com
datanalytic[.]org
expertglobal[.]org
only-music[.]net
popsonglist[.]com
querylight[.]net
smartstand[.]org
stylishblock[.]com
webs-update[.]com
```

## Filesystem indicators
```
C:\Windows\System32\migration\netiopmig.dll
C:\Windows\System32\migration\sppvmig.dll
C:\Windows\System32\migration\spvmig.dll
C:\Windows\System32\ime\imejp\imjpueact.dll
C:\Windows\System32\ime\imejp\imjpuexp.dll
C:\Windows\System32\ime\imetc\imtcprot.dll
C:\Windows\System32\ime\shared\imccphd.dll
C:\Windows\System32\ime\shared\imebrokev.dll
C:\Windows\System32\ime\shared\imecpmeid.dll
C:\Windows\System32\ime\shared\imepadsvd.dll
C:\Windows\System32\migration\imjprmig.dll
C:\Windows\System32\wbem\dmwmibridgeprov132.dll
C:\Windows\System32\wbem\esscli32.dll
C:\Windows\System32\wbem\netdacim32.dll
C:\Windows\System32\wbem\netpeerdistcim32.dll
C:\Windows\System32\wbem\viewprov32.dll
C:\Windows\System32\wbem\vsswmi32.dll
C:\Windows\System32\wbem\wbemcore32.dll
C:\Windows\System32\wbem\wbemdisp32.dll
C:\Windows\System32\wbem\wbemsvc32.dll
C:\Windows\System32\wbem\wfascim32.dll
C:\Windows\System32\wbem\win32_encryptablevolume32.dll
C:\Windows\System32\wbem\wmiaprpl32.dll
C:\Windows\System32\drivers\HW.sys
C:\Windows\System32\drivers\HW.sys.dat
```

All ".dll" files might also appear with an additional ".inf" extension (e.g. "C:\Windows\System32\migration\netiopmig.dll.inf")

## Hijacked CLSIDs
```
HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{4590F811-1D3A-11D0-891F-00AA004B2E24}\InprocServer32
	- legitimate default value: %systemroot%\system32\wbem\wbemprox.dll
HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{4FA18276-912A-11D1-AD9B-00C04FD8FDFF}\InprocServer32
	- legitimate default value: %systemroot%\system32\wbem\wbemcore.dll
HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{7C857801-7381-11CF-884D-00AA004B2E24}\InProcServer32
	- legitimate default value: %systemroot%\system32\wbem\wbemsvc.dll
HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{CF4CC405-E2C5-4DDD-B3CE-5E7582D8C9FA}\InprocServer32
	- legitimate default value: %systemroot%\system32\wbem\wmiutils.dll
```
