# IOC for Retadup

Malware analysis and more technical information at <https://decoded.avast.io/janvojtesek/putting-an-end-to-retadup-a-malicious-worm-that-infected-hundreds-of-thousands/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [Network indicators](#network-indicators)
* [File names](#file-names)
* [Registry keys](#registry-keys)
* [Mutexes](#mutexes)


## Samples (SHA-256)
#### AutoIt/AutoHotkey core:
```
a8ccb0a1c70975a1f34d0c40784e259e4c62c2533177f84ecd953c03106dd77e
b4d8d7cbec7fe4c24dcb9b38f6036a58b765efda10c42fce7bbe2b2bf79cd53e
c69811d8574fcc59e37fe2cbf0a31be4956ab81c3279bfb1351ff6da3417b4a7
668dafd68f33c589d0ceefac1d312632a64b2f5798e29a4701bf535a82251cc8
91b75ccd19e045c24eec0399bdf4ab504fc8ecee2514f16b29d50c2967d2ad87
```
#### AutoIt loaders:
```
94cdce276447b3339dcf90c90c05faa324fa7f5cc022d0f0538ff01e0a86486c
fb722e9df7c2c4dbade734c41f810699d8eb19573b05cb55fa235065ba545133
2bed949f0cfe04b88b75bac404dc191b24d224deead993a3c82f15fad88a39c8
```
#### AutoIt/AutoHotkey interpreters (not malicious itself):
```
77c2372364b6dd56bc787fda46e6f4240aaa0353ead1e3071224d454038a545e
1b5e7860c517ad4c70eb750e0f0eecd43a1cf90df3adc4b5195242ef8944e9e1
8498900e57a490404e7ec4d8159bee29aed5852ae88bd484141780eaadb727bb
```
#### HoudRat:
```
940bef003d57e3ef78fb7dd9ed0bb528611164dd663db80aa6d875a8b8688ef4
```
#### Retadup miner:
```
9c46a0e48ea9b104f982e5ed04735b0078938866e3822712b5a5374895296d08
36820a9c9e7b22a069fe897e3a82e05efad888150c0a91a6ef93fb139c702093
000506b6fb0d6e608910584d9b7d7b5da7105755b203a390087bf4637147e244
000e3af1ec99f4ce7269cc734d164e2c5a34a396f03c7a0190e46f47ccf0bf07
000e4f56bff7202d9741e435073e020ec74a02ec641555aab7a0d448354512d1
00154ca809565b7b65e72a17735efb86c0134539b8591f95e926aed3d4954426
```
#### Stop ransomware:
```
6a6a632e98e89a20b910961ba898cafb6651e88ee39187585be06496a31d5fc8
```
#### Arkei password stealer:
```
7bdf91007e233bc49cb8837c2d098a0cdb00c20e5a925181fe8d5d12153d36ca
```

## Network indicators
#### C&C servers (no longer pose any threat)
```
alphanoob[.]com
newalpha.alphanoob[.]com
newblackage[.]com
noobminer.newblackage[.]com
newminersage[.]com
newminer.newminersage[.]com
newage.newminersage[.]com
superuser.newminersage[.]com
superlover.newminersage[.]com
blackjoker.newminersage[.]com
superalpha.newminersage[.]com
newghoul2019.newminersage[.]com
radnewage[.]com
newage.radnewage[.]com
superalpha.radnewage[.]com
newghoul2019.radnewage[.]com
minernewage[.]com
newage.minernewage[.]com
mdwnte[.]com
rad2016.publicvm[.]com
hellothere.publicvm[.]com
radjoker2.publicvm[.]com
noobminer.publicvm[.]com
radpal.publicvm[.]com
newalpha.super-gamezer[.]com
roro2016.linkpc[.]net
```

#### Downloader urls
```
https://cdn.fbsbx[.]com/v/t59.2708-21/51240740_1526686477462685_3364590801735647232_n.txt/superstart.txt?_nc_cat=106&_nc_ht=cdn.fbsbx.com&oh=570ee08b0c9931f462fdafe8a0ac71a9&oe=5C878A28&dl=1&fbclid=IwAR0SGHmmh4wDShgQravm6Oc7TGs8a1qNBKPpLMkCilct7q_EVlH01AE3SDU
https://cdn.fbsbx[.]com/v/t59.2708-21/52725629_413032812781355_8785085076862926848_n.txt/superyaysource.txt?_nc_cat=111&_nc_ht=xxx.com&oh=de93756a8f1b622e11b7d39efc7cd8c3&oe=5C8B2F78&dl=1&id=IwAR110ZIu9CR-FLgLrJE-glQCfrHt6lhlF3dZ9swsBfcrAW5GHZYLVECOZLc
https://cdn.fbsbx[.]com/v/t59.2708-21/50228067_2272438499698319_9158831988499546112_n.txt/newsoso.txt?_nc_cat=101&_nc_ht=xxx.com&oh=817eb565cb90f236e4f5314a1c44c254&oe=5C54B577&dl=1&id=IwAR3Ge37MwyqvvR5IjhVPlGUSoOk1Aj-PG2WoiPZNcHPpdR-UvTrTtC_3yKs
https://cdn.fbsbx[.]com/v/t59.2708-21/53669254_2268996769806362_4859779336787460096_n.txt/newyayay.txt?_nc_cat=106&_nc_ht=xxx&oh=1f1072d71aa3fb84dac6151d8fb6a71d&oe=5CA36CDC&dl=1&id=IwAR26WTCOs1-yzAt4whJMvaCkrFOBmEr0owU23-4uUsbVMJvi0QvrHUAzrbE
https://cdn.fbsbx[.]com/v/t59.2708-21/51605394_1245620798922794_4863859761877090304_n.txt/soso.txt?_nc_cat=108&_nc_ht=xxx.com&oh=197debe4b87bb3eca6bfa8fea24d604b&oe=5C85C580&dl=1&id=IwAR0LqpMYGJIfC4zsLvnBZG9F8N-DUp9jf1zTkguqXEs6yf7-Xn8Gb8oAgQ4
https://cdn.fbsbx[.]com/v/t59.2708-21/60143633_352756602260509_7414425884448260096_n.a3x/sukablat.a3x?_nc_cat=110&_nc_ht=cdn.fbsbx.com&oh=4d3f9a333a6ce8cce6510795588a6526&oe=5CF268AE&dl=1&fbclid=IwAR06O_CctoumJ2K5SMU9_MUBD-Pof9ZTG6u6RmXtuoBvb32TWtys48PUEq0
http://ymad[.]ug/tesptc/ck/5475.exe
https://2no[.]co/1aSa97
http://newminer.newminersage[.]com:92/x64.exe
```

## File names
```
C:\streamer\streamer.exe
C:\streamer\stream.txt
C:\streamerdata\stream.txt
C:\newcpuspeedcheck\cpufix.exe
C:\newcpuspeedcheck\cpuage.tnt
C:\newcpuspeedcheck\workers\rad\cpuchecker.exe
C:\AntiShortCut\AntiUsb.exe
C:\AntiShortCut\AntiUsbShortCut.zip
C:\AntiShortCut\systeminfo\Infomisc.exe
C:\WinddowsUpdater\WinddowsUpdater.exe
C:\WinddowsUpdater\WinddowsUpdater.zip
%ProgramData%\\[a-zA-Z]{10}\\cfg
%ProgramData%\\[a-zA-Z]{10}\\cfgi
C:\\[a-z]{21}\\[a-z]{21}\.exe
C:\\[a-z]{21}\\[a-z]{21}\.txt
```

## Registry keys
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\flaterem
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\strdat
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\superlover
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\WinddowsUpdater
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\WinddowsUpdate
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\superloaver
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\radlover
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\CpuOptimizer
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Checkcpu
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\AntiUsbShortCut
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\AntiShortCutUpdate
HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\[a-z]{21}
```

## Mutexes
```
WinddowsUpdater
BlackJockerminer
BlackJockerChecker
BlackJockerNewAge
Socskettest
ff9702c705fd434610c0
65201cb96727ea7f03f7
bf73f1604fc0b6b3d70d
5f4038dd8be7d2633ba9
4b5c72a840be4f2291f2
```
