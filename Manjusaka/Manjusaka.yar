private rule ELF
{
	strings:
		$h01 = { 7F 45 4C 46 (01|02) (01|02) 01 }
	condition:
		$h01 at 0
}

private rule EXE
{
	condition:
		uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550
}

rule manjusaka_framework_go_build_id
{
	meta:
		author = "Avast Threat Intel Team"
		source = "https://github.com/avast/ioc"
		hash = "955e9bbcdf1cb230c5f079a08995f510a3b96224545e04c1b1f9889d57dd33c1" // ELF v01
		hash = "f275ca5129399a521c8cd9754b1133ecd2debcfafc928c01df6bd438522c564a" // ELF v02 upx
		hash = "637f3080526d7d0ad5eb41bf9331fb51aaafd30f2895c00a44ad905154f76d70" // ELF v02 unpacked
		hash = "b5c366d782426bad4ba880dc908669ff785420dea02067b12e2261dd1988f34a" // ELF v03 (dev) upx
		hash = "107b094031094cbb1f081d85ec2799c3450dce32e254bda2fd1bb32edb449aa4" // ELF v03 (dev) unpacked
		hash = "fb5835f42d5611804aaa044150a20b13dcf595d91314ebef8cf6810407d85c64" // ELF v03 upx
		hash = "ff20333d38f7affbfde5b85d704ee20cd60b519cb57c70e0cf5ac1f65acf91a6" // ELF v03 unpacked
		hash = "3581d99feb874f65f53866751b7874c106b5ce65a523972ef6a736844209043c" // MZ v03 upx
		hash = "6082bf26bcc07bf299a88eaa0272022418b12156cd987adfdff9fa1517afcf3d" // MZ v03 unpacked
		hash = "14dfb43a1782b0b8d93c3d67d63b6c786b0a223bc50c3ec68106bd18d43652a4" // ELF v04 upx
		hash = "4a0f47132867c12a6d009e43812729a1bb41f4eb83472ac352fc5b20fe937bef" // ELF v04 unpacked
		hash = "bb1b7d506559c783ed747da461f58ea5256ba0a083768ae6aa1a2325017c4387" // ELF v05 upx
		hash = "bd0e09e9ee4db74ada6433f00024a543f799046c15f635216ca4ae5e1f0c42e2" // ELF v05 unpacked
	strings:
		// ELF v01
		$h01 = { 47 6F 00 00 57 79 5F 76 69 62 44 5A 76 32 77 6D 35 62 4C 32 71 73 6A 4A 2F 34 50 4D 56 79 4D 39 39 76 61 76 58 68 7A 65 5A 34 6C 76 2D 2F 4E 59 6C 5F 4B 6D 75 53 45 62 53 4E 4A 6B 39 45 61 52 74 31 2F 2D 45 4D 50 57 64 6A 73 30 4E 6C 37 73 79 67 41 41 74 65 54 00 }
		// ELF v02 unpacked
		$h02 = { 47 6F 00 00 79 30 4D 57 35 6A 74 30 45 6B 61 77 55 4B 35 6B 6B 6C 31 32 2F 5A 68 34 34 36 61 65 4D 7A 62 48 47 37 4F 73 56 4F 66 71 75 2F 6D 5F 58 74 43 52 32 32 39 75 4B 67 5A 62 51 65 44 35 43 74 2F 66 78 66 47 4A 47 61 59 4E 31 5F 36 6E 4E 76 32 58 5A 53 62 00 }
		// ELF v02 upx
		$h03 = { 47 6F 06 FF FF FF 7F 79 30 4D 57 35 6A 74 30 45 6B 61 77 55 4B 35 6B 6B 6C 31 32 2F 5A 68 34 34 36 61 65 4D 7A 62 FF FF FF FF 48 47 37 4F 73 56 4F 66 71 75 2F 6D 5F 58 74 43 52 32 32 39 75 4B 67 5A 62 51 65 44 35 43 74 2F }
		// ELF v03 (dev) unpacked
		$h04 = { 47 6F 00 00 30 33 30 36 42 53 4B 42 71 6E 71 4B 74 4D 51 71 67 53 58 4D 2F 68 4C 6A 34 77 76 56 56 4A 4C 79 42 43 61 4A 42 5F 38 4D 30 2F 73 74 66 62 47 73 46 5A 58 67 4E 6B 50 77 5A 4B 4C 71 52 65 2F 4D 49 46 68 69 67 7A 65 50 53 65 56 35 64 5F 52 6D 66 43 35 00 }
		// ELF v03 (dev) upx
		$h05 = { 47 6F 06 FF FF FF 7F 30 33 30 36 42 53 4B 42 71 6E 71 4B 74 4D 51 71 67 53 58 4D 2F 68 4C 6A 34 77 76 56 56 4A 4C FF FF FF FF 79 42 43 61 4A 42 5F 38 4D 30 2F 73 74 66 62 47 73 46 5A 58 67 4E 6B 50 77 5A 4B 4C 71 52 65 }
		// ELF v03 unpacked
		$h06 = { 47 6F 00 00 36 35 34 67 69 6A 50 41 55 6B 45 61 7A 4A 70 6A 44 39 4E 55 2F 67 44 75 48 46 31 78 66 64 70 39 31 53 66 36 53 59 51 48 58 2F 76 73 6E 6E 37 65 6B 67 30 54 4B 58 57 69 4F 53 63 46 30 44 2F 53 61 6D 30 73 51 6D 66 79 43 61 44 43 38 71 43 66 59 78 35 00 }
		// ELF v03 upx
		$h07 = { 47 6F 06 FF ED FF 7F 36 35 34 67 69 6A 50 41 55 6B 45 61 7A 4A 70 6A 44 39 68 2F 67 44 75 48 46 31 78 66 FF FF FF FF 64 70 39 31 53 66 36 53 59 51 48 58 2F 76 73 6E 6E 37 65 6B 67 30 54 4B 58 57 69 4F 53 63 46 30 }
		// MZ v03 unpacked
		$h08 = { 47 6F 20 62 FF FF FF FF 75 69 6C 64 20 49 44 3A 20 22 65 72 52 47 4F 4A 56 48 65 38 37 58 67 6D 79 4F 56 77 48 44 2F 42 FB FF FF FF 70 78 56 76 70 79 44 58 74 4C 64 64 79 57 46 64 38 4E 39 2F 6F 59 77 64 70 73 6D 46 45 }
		// MZ v03 upx
		$h09 = { 47 6F 20 62 75 69 6C 64 20 49 44 3A 20 22 65 72 52 47 4F 4A 56 48 65 38 37 58 67 6D 79 4F 56 77 48 44 2F 42 70 78 56 76 70 79 44 58 74 4C 64 64 79 57 46 64 38 4E 39 2F 6F 59 77 64 70 73 6D 46 45 44 58 39 32 58 4A 55 52 4C 55 7A 2F 62 62 58 59 38 43 76 6B 44 4D 72 69 42 33 32 64 49 36 53 58 }
		// ELF v04 unpacked
		$h10 = { 47 6F 00 00 47 6E 42 4B 6F 63 4C 77 76 57 5A 6E 43 5F 55 6D 49 72 2D 72 2F 36 50 2D 4F 7A 46 62 51 37 39 6F 59 79 79 61 44 52 48 56 34 2F 38 74 6D 46 77 78 63 53 64 63 63 6D 70 66 73 5A 63 33 68 62 2F 77 34 2D 36 49 52 50 70 75 42 66 75 61 68 7A 50 63 4C 35 32 00 }
		// ELF v04 upx
		$h11 = { 47 6F 06 FF FF FF FF 6E 42 4B 6F 63 4C 77 76 57 5A 6E 43 5F 55 6D 49 72 2D 72 2F 36 50 2D 4F 7A 46 62 51 37 39 6F FF FF 6F FF 59 79 79 61 44 52 48 56 DC 38 74 6D 46 77 78 63 53 64 63 63 6D 70 66 73 5A 63 33 68 62 }
		// ELF v05 unpacked
		$h12 = { 47 6F 00 00 4E 50 57 41 64 50 62 57 6D 6E 58 72 30 61 36 67 44 37 4B 7A 2F 54 74 6E 59 64 4F 79 43 6A 76 63 43 51 75 5A 39 47 69 44 72 2F 46 43 6D 4F 69 38 41 30 36 36 52 50 43 36 53 4F 57 76 61 4D 2F 43 70 57 37 4F 30 73 38 61 51 32 42 46 56 64 66 65 62 54 4A 00 }
		// ELF v05 upx
		$h13 = { 47 6F 06 FF FF FF 7F 4E 50 57 41 64 50 62 57 6D 6E 58 72 30 61 36 67 44 37 4B 7A 2F 54 74 6E 59 64 4F 79 43 6A 76 FF FF FF FF 63 43 51 75 5A 39 47 69 44 72 2F 46 43 6D 4F 69 38 41 30 36 36 52 50 43 36 53 4F 57 76 61 4D 2F }
	condition:
		any of them
}

rule manjusaka_payload_encoded_hexstring
{
	meta:
		author = "Avast Threat Intel Team"
		source = "https://github.com/avast/ioc"
	strings:
		// ELF v01 and v02
		$s01 = "1f8b08000000000000ff7cdd099c1ae5fd3ff031e620c6038d5aea493df18a24c688372626c1180d468d78d465b34b96357be0ee2612354ab5553caa68ad454d158f2a566b51ab454d2dde"
		// ELF v03 (dev)
		$s02 = "1f8b08000000000000ff94dd09982355d9fffd62d89a45880a181621804240c10888718328a8ed864144a3029d66ba67d2cc4c4fecee8180a85114f3284b4096b00d619380085111f3284a"
		// ELF v03
		$s03 = "1f8b08000000000000ff94dd0b982355b5fffde21eee011503a204440d201001317a148278890a1804348ad269667a260d3d33b1bb19820246bc10914bb80811618c80108f084110232204"
		// ELF v04
		$s04 = "1f8b08000000000000ff94dd07981bd5d9fffdb131208a41b4075123ba280101c6112d88d04468a22b01b25abc6b6bf17aadecae4140008540103582001110401483e8a28b2e4a4074d197"
		// MZ v01
		$s11 = "1f8b08000000000000ffecbd09784cd7ff077c26c924631977828958c284694d5092da12eb8448ce302108a248628ba82d65862025e924b8aeabdaeaa2abb6bfaebad74f83fe4804a1d5d6"
		// MZ v02
		$s12 = "1f8b08000000000000ffecbd097414c5faff5d9d7502849e400209201974c4441113371240c8842cd5d00361070502224bdc403203a82c8993d1146d2b7ac5e5ba5cdcb9aea85c36176612"
		// MZ v03 (dev)
		$s13 = "1f8b08000000000000ffecbd7b7854d5d928be7632496620710d4874522e9991ad4e94627641491425031378b7ae1150046a1168a1237ca2419801542e893b53b3d8eeafb4b5777b8eb5fd"
		// MZ v03
		$s14 = "1f8b08000000000000ffecbd7b7854d5d530be4f32496620710f9ae8a45c3223479d28d51c414934960c4c601ddd23a811a845a0858e50d120cc002a97c49369b3399e96b6dacb5bfb7dbe"
		// MZ v04
		$s15 = "1f8b08000000000000ffecbd79785445d6305eb7934e3a90e676846887451abc68c7b5e33293284b37e924a7e506a222a022c45119501c23744b1c194ce6764b2a97abcc88233a3aaee38a"
	condition:
		(EXE or ELF) and (
			any of ($s0*) and
			any of ($s1*)
		)
}

rule manjusaka_payload_elf
{
	meta:
		author = "Avast Threat Intel Team"
		source = "https://github.com/avast/ioc"
		hash = "0063e5007566e0a7e8bfd73c4628c6d140b332df4f9afbb0adcf0c832dd54c2b" // 01, v02
		hash = "76eb9af0e2f620016d63d38ddb86f0f3f8f598b54146ad14e6af3d8f347dd365" // v03 (dev)
		hash = "0a5174b5181fcd6827d9c4a83e9f0423838cbb5a6b23d012c3ae414b31c8b0da" // v03
		hash = "63e7f6fa89faa88b346d0cceddf2ef2e3ebf5d5828aa0087663c227422041db7" // v04
		hash = "400855b63b8452221869630c58b7ab03373dabf77c0f10df635e746c13f98ea9" // v05
		hash = "4eb337c12f0e0ee73b3209bed4b819719c4af9f63f3e81dbc3bbf06212450f1c" // v05
	strings:
		$s01 = "proc/meminfo/proc/uptime/etc/os-releaseVERSION_ID=NAME=DISTRIB_ID"
		$s02 = "/root/.cargo/registry/src/mirrors.ustc.edu.cn"
		$s03 = "cmdlineexecwdassertion failed"
		$s04 = "/etc/passwd/root/"
		$s11 = "./protos/cs.rstargetpidAgentsagentAgentUpdatesleepenckeysysinfoConfigPluginExecPluginLoadReqCwd"
		$s12 = "ReqScreenH"
		$s13 = "manjusakahttp:"
		$s14 = "pluginexecpluginloadreqcwdreqcmd"
		$s15 = "/NPSC2/npc/libs/"
	condition:
		ELF and
		(
			all of ($s0*) and
			any of ($s1*)
		)
}

rule manjusaka_payload_mz
{
	meta:
		author = "Avast Threat Intel Team"
		source = "https://github.com/avast/ioc"
		hash = "6839180bc3a2404e629c108d7e8c8548caf9f8249bbbf658b47c00a15a64758f" // v01
		hash = "cd0c75638724c0529cc9e7ca0a91d2f5d7221ef2a87b65ded2bc1603736e3b5d" // v02
		hash = "d5918611b1837308d0c6d19bff4b81b00d4f6a30c1240c00a9e0a9b08dde1412" // v03 (dev)
		hash = "2b174d417a4e43fd6759c64512faa88f4504e8f14f08fd5348fff51058c9958f" // v03
		hash = "377bacba69d2bec770599ab21a202b574b92fb431fc35bbdf39080025d6cf2d6" //v04
		hash = "86c633467ba7981d3946a63184dbfabce587b571f761b3eb1e3e43f6b1df6f2c" //v05
		hash = "51857882d1202e72c0cf18ff21de773c2a31ee68ff28385f968478401c5ab4bb" //v05
		hash = "e07aa10f19574a856a4ac389a3ded96f2d78f41f939935dd678811bd12b5bd03" //v05
		hash = "9e7144540430d97de38a2adcef16ad43e23c91281462b135fcc56cafc2f34160" //v05
	strings:
		$s01 = ".\\protos\\cs.rstargetintranethostnameplatformpidAgentsstatusagentinternetupdateatAgentUpdate"
		$s02 = "PluginExecPluginLoadReqCwdcmdReqCmd"
		$s03 = "Users\\Administrator.WIN7-2021OVWRCZ\\.cargo"
		$s04 = "Users\\runneradmin\\.cargo"
		$s05 = "windows\\c.rsNtReadFile"
		$s11 = "src\\mirrors.ustc.edu.cn-"
		$s12 = "CodeProject\\hw_src\\NPSC2\\npc\\target\\release\\deps\\npc.pdb"
		$s13 = "@@@manjusaka"
		$s14 = "***manjusakahttp://"
		$s15 = "SELECT signon_realm, username_value, password_value FROM loginsnetshwlanshowprofile"
		$s16 = "name=key=clearWIFI"
		$s17 = "cmd.exe/c"
		$s18 = "Accept-Languagezh-CN,zh;q=0.9,en;q=0.8Accept-Encodinggzip"
		$s19 = "library\\std\\src\\sys_common\\wtf8.rs"
		$s110 = "plug_getpass_nps.dll"
		$s111 = "plug_test_nps.dll"
	condition:
		EXE and
		(
			2 of ($s0*) or
			3 of ($s1*)
		)
}
