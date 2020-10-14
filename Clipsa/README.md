# IOC for Clipsa

Malware analysis and more technical information at <https://decoded.avast.io/janrubin/clipsa-multipurpose-password-stealer/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [Network indicators](#network-indicators)
* [File names](#file-names)
* [Registry keys](#registry-keys)
* [Semaphores](#semaphores)


## Samples (SHA-256)
#### Clipsa binary and related files
```
2922662802EED0D2300C3646A7A9AE73209F71B37AB94B25E6DF57F6AED7F23E - condlg.exe
FD552E4BBAEA7A4D15DBE2D185843DBA05700F33EDFF3E05D1CCE4A5429575E5 - 65923_VTS.vob
A65923D0B245F391AE27508C19AC1CFDE7B52A7074898DA375389E4E6C7D3AE1 - condlg.dll
B56E30DFD5AED33E5113BD886194DD76919865E49F5B7069305034F6E0699EF5 - XMRig miner (C&C)
F26E5CA286C20312989E6BF35E26BEA3049C704471FF68404B0EC4DE7A8A6D42 - 65923_VTS.asx
```


## Network indicators
#### Downloader urls
```
poly.ufxtools[.]com/wp-content/plugins/WPSystem/dl.php?a=d
poly.ufxtools[.]com/wp-content/plugins/WPSystem/ok.php
```
#### Uploader urls
```
poly.ufxtools[.]com/wp-content/plugins/WPSecurity/up.php
```
#### C&C servers
```
http[:]//besttipsfor[.]com
http[:]//chila[.]store
http[:]//globaleventscrc[.]com
http[:]//ionix.co[.]id
http[:]//mahmya[.]com
http[:]//mohanchandran[.]com
http[:]//mutolarahsap[.]com
http[:]//northkabbadi[.]com
http[:]//poly.ufxtools[.]com
http[:]//raiz[.]ec
http[:]//rhsgroup[.]ma
http[:]//robinhurtnamibia[.]com
http[:]//sloneczna10tka[.]pl
http[:]//stepinwatchcenter[.]se
http[:]//topfinsignals[.]com
http[:]//tripindiabycar[.]com
http[:]//videotroisquart[.]net
http[:]//wbbministries[.]org
```


## File names
```
%APPDATA%\Roaming\AudioDG\condlg.exe
%APPDATA%\Roaming\AudioDG\zcondlg.exe
%APPDATA%\Roaming\AudioDG\log.dat
%APPDATA%\Roaming\AudioDG\log.dat
%APPDATA%\Roaming\AudioDG\obj\
%APPDATA%\Roaming\AudioDG\udb\
%APPDATA%\Roaming\AudioDG\rep.dat
```

## Registry keys
```
HCU\Software\Microsoft\Windows\CurrentVersion\Run\11f86284
```

## Semaphores
```
%APPDATA%\ROAMING\AUDIODG\CONDLG.EXE
%APPDATA%\ROAMING\AUDIODG\ZCONDLG.EXE
```

