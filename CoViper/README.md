# IoC for CoViper

Malware analysis and more technical informations at <https://decoded.avast.io/janrubin/coviper-locking-down-computers-during-lockdown/>


### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [File names](#file-names)
* [Registy keys](#registry-keys)


## Samples (SHA-256)
#### CoViper binary and related files
```
4FD9B85EEC0B49548C462ACB9EC831A0728C0EF9E3DE70E772755834E38AA3B3 - coronavirus.bat
C3F11936FE43D62982160A876CC000F906CB34BB589F4E76E54D0A5589B2FDB9 - end.exe
B780E24E14885C6AB836AAE84747AA0D975017F5FC5B7F031D51C7469793EABE - mainWindow.exe
C46C3D2BEA1E42B628D6988063D247918F3F8B69B5A1C376028A2A0CADD53986 - run.exe
A1A8D79508173CF16353E31A236D4A211BDCEDEF53791ACCE3CFBA600B51AAEC - Update.vbs
FE22DD2588666974CAE5B5BBDE2D763AFBD94BCCF72D350EC4E801F9354D103D - run.exe unpacked
DF1F9777FE6BEDE9871E331C76286BAB82DA361B59E44D07C6D977319522BA91 - run.bat
13C4423ED872E71990E703A21174847AB58DEC49501B186709B77B772CEEAB52 - cursor.cur
4A17F58A8BF2B26ECE23B4D553D46B72E0CDA5E8668458A80CE8FE4E6D90C42D - wallpaper.jpg
7AE5E2BE872510A0E2C01BCF61C2E2FB1E680CD9E54891D3751D41F53AC24F84 - New MBR
```

## File names
```
C:\COVID-19\coronavirus.bat
C:\COVID-19\end.exe
C:\COVID-19\mainWindow.exe
C:\COVID-19\run.exe
C:\COVID-19\Update.vbs
C:\COVID-19\cursor.cur
C:\COVID-19\wallpaper.jpg
```

## Registry keys
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v disabletaskmgr /t REG_DWORD /d 1 /f
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v wallpaper /t REG_SZ /d %homedrive%\COVID-19\wallpaper.jpg /f
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop /v NoChangingWallPaper /t REG_DWORD /d 1 /f
HKCU\Control Panel\Cursors /v Arrow /t REG_SZ /d %homedrive%\COVID-19\cursor.cur /f
HKCU\Control Panel\Cursors /v AppStarting /t REG_SZ /d %homedrive%\COVID-19\cursor.cur /f
HKCU\Control Panel\Cursors /v Hand /t REG_SZ /d %homedrive%\COVID-19\cursor.cur /f
HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v CheckForUpdates /t REG_SZ /d %homedrive%\COVID-19\Update.vbs /f
HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v explorer.exe /t REG_SZ /d %homedrive%\COVID-19\run.exe /f
HKLM\software\Microsoft\Windows\CurrentVersion\Run /v GoodbyePC! /t REG_SZ /d %homedrive%\COVID-19\end.exe /f
```
