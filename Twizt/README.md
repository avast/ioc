# IOC for Twizt
Twizt botnet is infiltrating `SMB` on port 139 through the `WNetAddConnection2W` API. Employing brute force tactics with hardcoded credentials, the attackers focus on compromising the `$ADMIN` resource.

Notably, the Twizt botnet exhibits a dynamic strategy by generating targets randomly. 
The cracked credentials are promptly transmitted to C2. So, the result of this effort can be a successful exploit of vulnerable systems.


### Table of Contents
* [Hardcoded Credentials](#hardcoded-credentials)
* [Samples (SHA-256)](#samples-sha-256)
* [Network indicators](#network-indicators)


## Hardcoded Credentials
#### Usernames
```
Administrator
administrator
Admin
Administrator
admin
admin1
admin12
admin123
```

#### Passwords
[passwords](smb-passwords.txt)


## Samples (SHA-256)
#### Twizt Bot
```
A306D86351AB6783E2806F88DFC663357FA1B4750A68347FCD73250AB3AFC90F
```


## Network indicators
#### C&C server
```
http[:]//185.215.113[.]66
```
#### Uploader URL
```
hxxp://185.215.113[.]66/admin.php?s=<attacked_domain>|<password>|<user>
```
