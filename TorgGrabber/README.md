# IoC for Torg Grabber

Malware analysis and more technical information at <https://www.gendigital.com/blog/insights/research/torg-grabber-credential-stealer-analysis>

### Table of Contents
* [Samples (SHA-256)](#samples-sha-256)
* [C2 Domains](#c2-domains)
* [Delivery Infrastructure](#delivery-infrastructure)
* [Telegram Bot Tokens](#telegram-bot-tokens)
* [Network Signatures](#network-signatures)
* [Host Indicators](#host-indicators)
* [Extras](#extras)

## Samples (SHA-256)

310 samples. Full list in [`samples.sha256`](samples.sha256).

#### Representative samples
```
aadf26ddea3c499b54e978347ff0ec394af15515a02de5e819a8c396e455a02e
4c901933c2f39b9eecd33e03af127226a1e41bfd033833f7bb3b49fa12a3dab9
0f217cae05a7e5882cafc681e5ca6f3ba51243cf7ccfedb7e5d5c836281f0f36
eaf0a66d8fffffd4b05cf57a35e7139003a81ac2896c392fdc762719767118ac
82e1ee932b1b50e0c600a14bc0bbed70d4825cf424aa133087bd05078667d1ab
6747f1d9ee75b0c605b68aad2c15fa268228260f7378290a3dff83dde24096c7
5529aeff146c3a388dd4047e04e355922e80e7a414971d6a8b944a15cf9691f9
```

## C2 Domains

Full list with comments in [`network.txt`](network.txt).

#### Stealer C2 (REST API)
```
gogenbydet[.]cc
technologytorg[.]com
attackzombie[.]com
evasivestars[.]com
safeguss[.]com
sinixproduction[.]com
startbuldingship[.]com
findyour-dreams[.]com
wulingyuanparkzone[.]com
new-app-techno[.]com
bbcplay[.]top
playbergs[.]info
avanpost-fi[.]digital
si-dodgei[.]digital
```

#### Stealer C2 (machine_api backend)
```
quick-neo[.]com
50elk[.]com
```

#### GRAB TCP protocol (port 50443)
```
bk.tara[.]net[.]bd
raketa.tara[.]net[.]bd
```

## Delivery Infrastructure

```
j0o[.]pw
t4e[.]pw
re3[.]pw
```

IP: `84.200.125.231`

## Telegram Bot Tokens

```
8247426625:AAFM5NrhXSFhcZ1HL-nMY_1mQtZ6AnAA4KM
8284437818:AAEPpXIyKB6Jsn4AYAArlfzEaaBEno_uV_0
8378862166:AAEasf-A6giPlk9SJpPN-Ar6pmsdfPuUx8M
8456437646:AAHpe9SdXev4Yc5GbWLvxElNnJNczhKqiGA
8456665882:AAGjdnjog6vE0XkfMAMt_L7oNlIPKDg_smI
8471726820:AAE8W2Fj1-hXMAnqXn_zg6cDZMZsSmGqXuo
8481173620:AAHpZlGmLscLpf9k_fcdNN8UG0Kk2cXg_tg
8541391788:AAGxUxLQGZuElDtJl21cstuwKwfiO4680F4
```

## Network Signatures

```
URI: /api/auth
URI: /api/upload/start, /api/upload/chunk, /api/upload/complete
URI: /api/stream/file, /api/stream/complete
URI: /api/ping
URI: /api/machine/set-files-r (machine_api variant)
Headers: X-Auth-Token, X-Upload-Id, X-Offset, X-Session, X-File-Path
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

## Host Indicators

```
Environment variables: GRABBER_HOST, GRABBER_TAG, GRABBER_SESSION
Environment variables: GRABBER_ANTI_SNG, GRABBER_ANTI_VM, GRABBER_STREAMING
Mutex: Local\<MachineGuid>
Debug string: "[#] Build: grabber v1.0"
Dropper path: C:\Windows\<random_alphanum>.exe
```

## Extras

| File | Description |
|------|-------------|
| [`extras/wallet_extensions.txt`](extras/wallet_extensions.txt) | 728 targeted crypto wallet browser extensions (ID and name) |
| [`extras/password_extensions.txt`](extras/password_extensions.txt) | 103 targeted password manager / 2FA browser extensions |
| [`extras/notes_extensions.txt`](extras/notes_extensions.txt) | 19 targeted notes browser extensions |
| [`extras/targeted_browsers.txt`](extras/targeted_browsers.txt) | 25 Chromium + 8 Firefox browsers with profile paths |
| [`extras/targeted_apps.txt`](extras/targeted_apps.txt) | Desktop wallets, VPN, FTP, email, gaming apps targeted |
