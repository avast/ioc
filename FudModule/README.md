# IoC for FudModule

GenDigital's full FudModule v3 report is available at <https://www.gendigital.com/blog/preview/lazarus-fudmodule>
Avast's full FudModule report is available at <https://decoded.avast.io/janvojtesek/lazarus-and-the-fudmodule-rootkit-beyond-byovd-with-an-admin-to-kernel-zero-day/>

### Table of Contents
* [YARA](#yara)
* [Targeted ETW Provider GUIDs](#targeted-etw-provider-guids)


## YARA

```
rule fudmodule_v2_sequences
{
    meta:
        reference = "https://decoded.avast.io/janvojtesek/lazarus-and-the-fudmodule-rootkit-beyond-byovd-with-an-admin-to-kernel-zero-day/"
    strings:
        $s00 = "overwrite pvmode failed. %X"
        $s01 = "%s\\temp\\tem1245.tmp"
        $s02 = "get NTKernelBase and some DriverBase failed."
        $s03 = "ClearVaccineNotifyRoutine failed."
        $s04 = "DisableUserEtwSource (%d/%d) passed."
        $s05 = "ClearVaccineNetworkFilterRoutine skipped."

        $h00 = {65 48 8B 04 25 30 00 00 00 48 8B CB 48 8B 50 60 48 89 13 80 7A 02 01 75 16 48 8D 15 ?? ?? ?? ?? E8 ?? ?? ?? ?? B8 01 00 00 F0 E9}
        $h01 = {48 C7 81 F0 00 00 00 20 01 00 00 48 C7 81 F8 00 00 00 A0 00 00 00 48 C7 81 08 01 00 00 A0 00 00 00 48 C7 81 18 01 00 00 68 00 00 00 48 C7 81 20 01 00 00 40 00 00 00}
        $h02 = {05 9F B5 FF FF 83 F8 04 0F 87 ?? ?? ?? ?? 48 C7 81 28 01 00 00 80 10 00 00}
        $h03 = {48 A3 08 00 00 80 00 00 00 00 48 8B 43 38 48 8B 4B 60}
        $h04 = {C7 45 ?? 65 72 53 69 C7 45 ?? 6C 6F 4E 61 66 C7 45 ?? 6D 65 C6 45 ?? 00 66 C7 45 ?? 48 8D}
        $h05 = {66 C7 45 ?? 4C 8B C6 45 ?? 3D 66 C7 45 ?? 48 8D C6 45 ?? 05 C7 45 ?? 46 6C 74 45 C7 45 ?? 6E 75 6D 65}
    condition:
        2 of them
}

rule fudmodule_v3_sequences
{
	meta:
		author = "Luigino Camastra, GenDigital"
		reference = "https://www.gendigital.com/blog/preview/lazarus-fudmodule"
	strings:
		$s00 = "Success." // 0x14001acf0
		$s01 = "remote_exec failed." // 0x14001ad00
		$s02 = "init_env failed." // 0x14001ac90
		$s03 = "GetGodMode failed" // 0x14001acc0
		$s04 = "RemoteDllExecute passed." // 0x14001b268
		$s05 = "CreateRemoteProcess passed." // 0x14001b220
		$s06 = "GetSystemHandle passed." // 0x14001b208
		$s07 = "SuspendDefender skipped." // 0x14001b1b8
		$s08 = "DisableUserEtwSource (%d/%d) passed." // 0x14001b180
		$s09 = "EtwpHostSiloState is Null." // 0x14001b140
		$s10 = "Get EtwpHostSiloState failed." // 0x14001b160
		
		$h00 = { 8A 44 0E ?? 41 32 C4 88 01 B0 0D 48 FF C1 41 F6 }
		$h01 = { 4? 8B DF 4? 8D 47 D0 4? C1 E0 10 4? C1 E3 10 4? }
		$h02 = { B? 05 00 00 00 4? 81 E3 FF FF 0F 00 4? 33 D8 4C }
	condition:
		3 of them
}

```

## Targeted ETW Provider GUIDs
Note: This is a list of legitimate GUIDs that are targeted by FudModule in its "0x80" rootkit technique.
```
{555908d1-a6d7-4695-8e1e-26931d2012f4}
{0063715b-eeda-4007-9429-ad526f62696e}
{eef54e71-0661-422d-9a98-82fd4940b820}
{54849625-5478-4994-a5ba-3e3b0328c30d}
{099614a5-5dd7-4788-8bc9-e29f43db28fc}
{ef1cc15b-46c1-414e-bb95-e76b077bd51e}
{1edeee53-0afe-4609-b846-d8c0b2075b1f}
{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}
{b977cf02-76f6-df84-cc1a-6a4b232322b6}
{de7b24ea-73c8-4a09-985d-5bdadcfa9017}
{7d44233d-3055-4b9c-ba64-0d47ca40a232}
{bde46aea-2357-51fe-7367-d5296f530bd1}
{245f975d-909d-49ed-b8f9-9a75691d6b6b}
{43d1a55c-76d6-4f7e-995c-64c711e5cafe}
{6ad52b32-d609-4be9-ae07-ce8dae937e39}
{f4aed7c7-a898-4627-b053-44a7caa12fcd}
{b447b4db-7780-11e0-ada3-18a90531a85a}
{b447b4dc-7780-11e0-ada3-18a90531a85a}
{b447b4dd-7780-11e0-ada3-18a90531a85a}
{b447b4de-7780-11e0-ada3-18a90531a85a}
{b447b4df-7780-11e0-ada3-18a90531a85a}
{b447b4e0-7780-11e0-ada3-18a90531a85a}
{b447b4e1-7780-11e0-ada3-18a90531a85a}
{f717d024-f5b4-4f03-9ab9-331b2dc38ffb}
{e595f735-b42a-494b-afcd-b68666945cd3}
{aea1b4fa-97d1-45f2-a64c-4d69fffd92c9}
{bd2f4252-5e1e-49fc-9a30-f3978ad89ee2}
{dd5ef90a-6398-47a4-ad34-4dcecdef795f}
{7b6bc78c-898b-4170-bbf8-1a469ea43fc5}
{e0c6f6de-258a-50e0-ac1a-103482d118bc}
{cdead503-17f5-4a3e-b7ae-df8cc2902eb9}
{11c5d8ad-756a-42c2-8087-eb1b4a72a846}
{62de9e48-90c6-4755-8813-6a7d655b0802}
{3ff37a1c-a68d-4d6e-8c9b-f79e8b16c482}
{ac43300d-5fcc-4800-8e99-1bd3f85f0320}
{a0c1853b-5c40-4b15-8766-3cf1c58f985a}
{30336ed4-e327-447c-9de0-51b652c86108}
{3cb2a168-fe19-4a4e-bdad-dcf422f13473}
{2f07e2ee-15db-40f1-90ef-9d7ba282188a}
{e7558269-3fa5-46ed-9f4d-3c6e282dde55}
{87a623f0-8db5-5c11-7c80-a2ebbcbe5189}
{dbe9b383-7cf3-4331-91cc-a3cb16a3b538}
{9d55b53d-449b-4824-a637-24f9d69aa02f}
{1ac55562-d4ff-4bc5-8ef3-a18e07c4668e}
{dd70bc80-ef44-421b-8ac3-cd31da613a4e}
{0ead09bd-2157-539a-8d6d-c87f95b64d70}
{1f678132-5938-4686-9fdc-c8ff68f15c85}
{1418ef04-b0b4-4623-bf7e-d74ab47bbdaa}
{1c95126e-7eea-49a9-a3fe-a378b03ddb4d}
{988c59c5-0a1c-45b6-a555-0c62276e327d}
{9e9bba3c-2e38-40cb-99f4-9e8281425164}
{e13c0d23-ccbc-4e12-931b-d9cc2eee27e4}
{d48ce617-33a2-4bc3-a5c7-11aa4f29619e}
{a70ff94f-570b-4979-ba5c-e59c9feab61b}
{f33959b4-dbec-11d2-895b-00c04f79ab69}
{393da8c0-dbed-11d2-895b-00c04f79ab69}
{e7ef96be-969f-414f-97d7-3ddb7b558ccc}
{609151dd-04f5-4da7-974c-fc6947eaa323}
{11cd958a-c507-4ef3-b3f2-5fd9dfbd2c78}
{e4b70372-261f-4c54-8fa6-a5a7914d73da}
{2a576b87-09a7-520e-c21a-4942f0271d67}
{cfeb0608-330e-4410-b00d-56d8da9986e6}
{0a002690-3839-4e3a-b3b6-96d8df868d99}
{751ef305-6c6e-4fed-b847-02ef79d26aef}
{8e92deef-5e17-413b-b927-59b2f06a3cfc}
{f4e1897c-bb5d-5668-f1d8-040f4d8dd344}
{fae10392-f0af-4ac0-b8ff-9f4d920c3cdf}
{70eb4f03-c1de-4f73-a051-33d13d5413bd}
{22fb2cd6-0e7b-422b-a0c7-2fad1fd0e716}
{7dd42a49-5329-4832-8dfd-43d979153a88}
{d1d93ef7-e1f2-4f45-9943-03d245fe6c00}
{45eec9e5-4a1b-5446-7ad8-a4ab1313c437}
{16a1adc1-9b7f-4cd9-94b3-d8296ab1b130}
{a68ca8b7-004f-d7b6-a698-07e2de0f1f5d}
{e02a841c-75a3-4fa7-afc8-ae09cf9b7f23}
{edd08927-9cc4-4e65-b970-c2560fb5c289}
{c7bde69a-e1e0-4177-b6ef-283ad1525271}
{7f54ca8a-6c72-5cbc-b96f-d0ef905b8bce}
{85a62a0d-7e17-485f-9d4f-749a287193a6}
{abf1f586-2e50-4ba8-928d-49044e6f0db7}
{b675ec37-bdb6-4648-bc92-f3fdc74d3ca2}
{8c416c79-d49b-4f01-a467-e56d3aa8234c}
{16c6501a-ff2d-46ea-868d-8f96cb0cb52d}
{b6d775ef-1436-4fe6-bad3-9e436319e218}
{65a1b6fc-4c24-59c9-e3f3-ad11ac510b41}
{fae96d09-ade1-5223-0098-af7b67348531}
{450bba94-53ce-54e6-d150-9636aceafb86}
{541dae91-cc3c-5807-b064-c2561c16d7e8}
{efb251e4-d454-4a02-b126-7fbb9d3991c3}
{047a1ff9-f05f-92ff-e8cc-94fc2ad7dce4}
{982a041a-49d0-4146-bc4a-a45ab395bdd5}
{57840c25-fa99-4f0d-928d-d81d1851e3dd}
{ed2bb9ad-e9a2-32a0-937b-6dd7b1bcf22b}
{07a88c90-6eda-4f36-0a2f-70d7006e5482}
{61e62ce2-b6bc-0000-80b0-1e700e81ffff}
```
