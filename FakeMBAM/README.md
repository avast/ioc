# IOC for FakeMBAM

Malware analysis and more technical information at <https://decoded.avast.io/janvojtesek/fakembam-backdoor-delivered-through-software-updates/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [Network indicators](#network-indicators)
* [File names](#file-names)
* [Registry keys](#registry-keys)


## Samples (SHA-256)
#### FakeMBAM installer/FakeMBAM backdoor
```
391817d625e14d6b5b0115b7215c07d9ef6612cccdb1d6891626fdd5609506bf Qt5Help.dll
02be0f263b95017caa20f0fed861d2126e81ec176d542cc7415074f48965f2e0 Qt5WinExtras.dll
dfb1a78be311216cd0aa5cb78759875cd7a2eeb5cc04a8abc38ba340145f72b9 MBSetup2.exe
f2caa14fd11685ba28068ea79e58bf0b140379b65921896e227a0c7db30a0f2c MBSetup.exe
```

#### Miner payloads
```
c6a8623e74f5aad94d899770b4a2ac5ef111e557661e09e62efc1d9a3eb1201c C:\ProgramData\VMware\VMware Tools\vmmem.exe
fea67139bc724688d55e6a2fde8ff037b4bd24a5f2d2eb2ac822096a9c214ede C:\ProgramData\VMware\VMware Tools\vmtoolsd.exe
b3755d85548cefc4f641dfb6af4ccc4b3586a9af0ade33cc4e646af15b4390e7 C:\ProgramData\VMware\VMware Tools\vm3dservice.exe
7f7b6939ae77c40aa2d95f5bf1e6a0c5e68287cafcb3efb16932f88292301a4d C:\ProgramData\VMware\VMware Tools\vm3dservice.exe
c90899fcaab784f98981ce988ac73a72b0b1dbceb7824f72b8218cb5783c6791 C:\ProgramData\VMware\VMware Tools\vmtoolsd.exe
a4447559249f3ce04be4c6d28fc15946cbb8513da76ba522f635bda6a60bedcc C:\ProgramData\VMware\VMware Tools\vmtoolsd.exe
8536d573c4180f5df09f183b9434636127127b2134fbf5dced0360ec6d4ee772 C:\ProgramData\VMware\VMware Tools\vmtoolsd.exe
61b194c80b6c2d2c97920cd46dd62ced48a419a09179bae7de3a9cfa4305a830 C:\ProgramData\VMware\VMware Tools\VMwareHostOpen.exe
589377832b1f1e6be2bdbef1753f30e3907c89a680f7f327999d9a1b510aa4ae C:\ProgramData\Mega Tools\ServiceHub.CLR.x64.exe
d7a06cba490da60cfbf6f120c33652393f7a1b9176170e57c6cc3649530fca6a C:\ProgramData\Sega Tools\ServiceHub.CLR.x64.exe
af49b57c1fc4781a7a38457c0b4a595dbb6b5bd7bc4ccafe15fb6b8ae29e17f8 C:\ProgramData\Sega Tools\ServiceHub.CLR.x64.exe
55869621fb2321ab8c8684d10c49e50e6a0b131f215ac0bbfe7c398d08fbea34 C:\ProgramData\Sega Tools\ServiceHub.CLR.x64.exe
f761242dfa8cf57faaae2c659f450bcbdc3253134556141eb6e0e282fbd98aa1 C:\ProgramData\Packages\Sega.549981C3F5F10_8wekyb3d8bbwe\ServiceHub.CLR.x64.exe
269e14bb368ef26f47416a8fcd7f556bece57f5b6113986dc733c2230efdf398 C:\ProgramData\USOPrivate\SearchApp.exe
beb718a13ef88b2d7f2126226217e76ea773af609aeae870f55e8eb6ed4c497b C:\ProgramData\Package\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\SearchApp.exe
70830ed1357efd6b373faeaa52701369e2ae7bf9ad74e2f9355b5499ecef1123 C:\ProgramData\USOPrivate\SearchApp.exe
277cb64e6cd1155c21f6f169d77036ea6e4a36288494f2dfc39d2e76191197d9 C:\ProgramData\USOPrivate\SearchApp.exe
f8288ecb42478dd37335669a956b4e1adb3400928e1ec440a24882163a9cbbe8 C:\ProgramData\USOPrivate\SearchApp.exe
edd918e7fe5dbb8e66464939c4a62132d5a3ba17d081c56f0a23beffb2c0ca0c C:\ProgramData\USOPrivate\SearchApp.exe
4c36a69540ffb7ac3655170148fe9f358bf0fc926baa7ef96611a7688727f76f C:\ProgramData\USOPrivate\SearchApp.exe
468968df636c3a3b7ef85b0ff528aeb403eaae7c943e4eebfbe5b98de19ff711 C:\ProgramData\USOPrivate\SearchApp.exe
a10277ffaec4e691cb1fa51fd65d2b7e045b138b0689ad7f5e0b79d855822df6 C:\ProgramData\USOPrivate\SearchApp.exe
```

#### data.pak
```
3036593e424bd4628593131b445408ba6a4039ef08e2fcdda1558010cc39ef37 data.pak
43bcec1d5149d43afbb4439eb88f59dcdbf1de363828a022e4a0b6474440223c data.pak
503e1b04708db7bf22935beee235965e503c370692904fb0c37344fd29696036 data.pak
624ae4069182064f1801beec52dee3195f15a306ccaaba4a798a5b1823fe0df8 data.pak
709e71ec3837520552e76c72796c6422a0713da88e227ac423d80e6f727c32a9 data.pak
7223641157529b6152503f4cf3cd2bbe358e325ebf0cef3b3930e058012c9de4 data.pak
768ceff0ddc67c5ea8858c6b1e80ddcac0907ded692efd33502c85eff370852a data.pak
893b242669d076f2460a789f951611dc58ab73c47f7b582fe504d7ecd0d18f29 data.pak
931e705984f60011b18aa0c38fb18f2040b87233dd94b506e7f20e504da58b6d data.pak
97e57ce2aded883a2eefc4a5cf60d162b98a3637abb2424e77083820c76422fa data.pak
97f8cd6db13a4e17d1aa84ce8950c153156b50f2eb29f5e3cd1a4496f50e7e0a data.pak
9734166814c8db737d472241e72bde437236da59a94d4991bb81589ce9271fad data.pak
```

## Network indicators
#### C&C URLs
```
https://apis.bytestech[.]dev/get/data
https://apis.mbytestech[.]com/get/data
https://apis.masterbyte[.]nl/get/data
https://d3ko3huol26z6z.cloudfront[.]net/get/data
https://d1t8lqzz4q8388.cloudfront[.]net/get/data
https://agonistatdata[.]site/get/data
https://apolistatdata[.]site/get/data
https://augustatdata[.]site/get/data
https://dq96vx43jmub5.cloudfront[.]net/get/data
```

#### Download URLs
```
http://dl.bytestech[.]dev/1/mbsetup.exe
http://dl.bytestech[.]dev/2/mbsetup.exe
http://dl.bytestech[.]dev/3/mbsetup.exe
http://dl.bytestech[.]dev/mbsetup2.exe
http://dl.cloudnetbytes[.]com/3/mbsetup.exe
```
#### Private mining pool IP addresses
```
142.4.214[.]15
164.90.228[.]90
134.122.75[.]91
134.122.95[.]252
188.124.36[.]164
54.93.189[.]78
18.184.46[.]95
35.180.226[.]235
46.101.118[.]136
46.101.195[.]40
185.132.176[.]153
139.59.156[.]70
15.236.226[.]247
46.101.120[.]189
34.254.170[.]193
18.159.45[.]239
52.57.156[.]29
134.122.77[.]49
35.180.36[.]209
```


## File names
```
%ProgramFiles%\Malwarebytes\Qt5Help.dll
%ProgramFiles(x86)%\Malwarebytes\Qt5Help.dll
%ProgramFiles%\Malwarebytes\data.pak
%ProgramFiles(x86)%\Malwarebytes\data.pak
%ProgramData%\VMware\VMware Tools\vmmem.exe
%ProgramData%\VMware\VMware Tools\vmtoolsd.exe
%ProgramData%\VMware\VMware Tools\vm3dservice.exe
%ProgramData%\VMware\VMware Tools\vmtoolsd.exe
%ProgramData%\VMware\VMware Tools\VMwareHostOpen.exe
%ProgramData%\Mega Tools\ServiceHub.CLR.x64.exe
%ProgramData%\Sega Tools\ServiceHub.CLR.x64.exe
%ProgramData%\Packages\Sega.549981C3F5F10_8wekyb3d8bbwe\ServiceHub.CLR.x64.exe
%ProgramData%\Package\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\SearchApp.exe
```

## Registry keys
```
HKLM\SOFTWARE\Wow6432Node\Malwarebytes\LicenseKey
HKLM\SOFTWARE\Malwarebytes\LicenseKey
```
