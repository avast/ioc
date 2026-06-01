# IoCs for Vidar

The repository includes the following scripts in the `extras` folder:

- `vidar_config_extractor.py` - statically locates the XOR-encrypted config blob in a Vidar sample and dumps the version, build_id, and C2 records (url, tag, user_agent).
- `vidar_decrypt_emu.py` - IDA + Unicorn script that finds Vidar's string-decryption trampolines via a byte pattern, emulates each call site to recover the plaintext, and annotates the results as IDA/Hex-Rays comments.

## Samples (SHA-256)

```
af992d4a96d5fcbdf3b0cd1783234ceb5ad9c2037349ec8a82e6d1aa7f2f0148 (Vidar v18.7)
4ed9e2f720e4f23ff0e57a1a032152f0452008da3447b7265d780cee3221c027 (Vidar v1.0)  <--- Vidar changed versioning of their builds
ec6f4f05575a6e7401e167a8a0f2506a6755c2d832deb63a0a5ff027d5ee6c5d (Vidar v1.1)
5788e98d4f9dd24f6ff9797832229c9096cadd108aaabef8d6737aad111f77c6 (Vidar v1.2)
f9ef434791a0b9b8b5f2472a666febbbef46dc5bc196706173fa2111909fae10 (Vidar v1.3)
e130a62564efaff95fb43590e431114bb384a2a94215d07da6ce696c7709a369 (Vidar v1.4)
a9dc6cfa821c1c0d75c18fc8e07554bc8ad778ad49c39b0bbe38101c09c289b5 (Vidar v1.5)
------------------------------------------------------------------------------
296c97d66ac4cb05777f053fa2c17e78b415567e449d169aa3cf683a6565d28a (Vidar v1.5)  <--- Vidar reworked (duplicit label v1.5)
16911bd74f0d6751a30a1be56a3752daf7bf333c0d6ec61d8746646dbe2a530d (Vidar v1.6)
27d4ad97468fa0388bc704a32dd5c5e21e6b1de76a160fbd2615530c58aa74a6 (Vidar v1.7)
155f9f56fcdab7dd03740656eaa27000ad68f76a4f7b4933fa57416278e909a7 (Vidar v1.8)
```
