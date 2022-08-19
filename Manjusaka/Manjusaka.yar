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
		// MZ v01
		$s11 = "1f8b08000000000000ffecbd09784cd7ff077c26c924631977828958c284694d5092da12eb8448ce302108a248628ba82d65862025e924b8aeabdaeaa2abb6bfaebad74f83fe4804a1d5d6"
		// MZ v02
		$s12 = "1f8b08000000000000ffecbd097414c5faff5d9d7502849e400209201974c4441113371240c8842cd5d00361070502224bdc403203a82c8993d1146d2b7ac5e5ba5cdcb9aea85c36176612"
		// MZ v03 (dev)
		$s13 = "1f8b08000000000000ffecbd7b7854d5d928be7632496620710d4874522e9991ad4e94627641491425031378b7ae1150046a1168a1237ca2419801542e893b53b3d8eeafb4b5777b8eb5fd"
		// MZ v03
		$s14 = "1f8b08000000000000ffecbd7b7854d5d530be4f32496620710f9ae8a45c3223479d28d51c414934960c4c601ddd23a811a845a0858e50d120cc002a97c49369b3399e96b6dacb5bfb7dbe"
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
	strings:
		$s01 = "proc/meminfo/proc/uptime/etc/os-releaseVERSION_ID=NAME=DISTRIB_ID"
		$s02 = "/root/.cargo/registry/src/mirrors.ustc.edu.cn"
		$s03 = "cmdlineexecwdassertion failed"
		$s04 = "/etc/passwd/root/"
		$s11 = "./protos/cs.rstargetpidAgentsagentAgentUpdatesleepenckeysysinfoConfigPluginExecPluginLoadReqCwd"
		$s12 = "ReqScreenH"
		$s13 = "manjusakahttp:"
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
	strings:
		$s01 = ".\\protos\\cs.rstargetintranethostnameplatformpidAgentsstatusagentinternetupdateatAgentUpdate"
		$s02 = "PluginExecPluginLoadReqCwdcmdReqCmd"
		$s03 = "Users\\Administrator.WIN7-2021OVWRCZ\\.cargo"
		$s11 = "src\\mirrors.ustc.edu.cn-"
		$s12 = "CodeProject\\hw_src\\NPSC2\\npc\\target\\release\\deps\\npc.pdb"
		$s13 = "@@@manjusaka"
		$s14 = "***manjusakahttp://"
		$s15 = "SELECT signon_realm, username_value, password_value FROM loginsnetshwlanshowprofile"
		$s16 = "name=key=clearWIFI"
		$s17 = "cmd.exe/c"
		$s18 = "Accept-Languagezh-CN,zh;q=0.9,en;q=0.8Accept-Encodinggzip"
	condition:
		EXE and
		(
			2 of ($s0*) or
			3 of ($s1*)
		)
}

