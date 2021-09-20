import idautils
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import hashlib
import base64

def KSA(key: bytes) -> bytes:
    S = bytearray(256)
    for i in range(256):
        S[i] = i
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
    return S

def PRGA(key: bytes, ci: bytes) -> bytes:
    S = KSA(key)
    a = 0
    b = 0
    pl = bytearray(len(ci))
    for i in range(len(ci)):
        a = (a+1) % 256
        b = (b + S[a]) % 256
        temp = S[a]
        S[a] = S[b]
        S[b] = temp
        K = S[(S[a] + S[b]) % 256]
        pl[i] = ci[i] ^ K
    return pl

def rc4_decrypt_str(citext, key):
    citext = bytearray.fromhex(citext.decode('utf-8'))
    pltext = PRGA(key, citext)
    return pltext

   
    return pltext

def xor_decrypt_str(citext, key):
    citext = bytearray.fromhex(citext.decode('utf-8'))
    pltext = bytearray()

    for i in range(0, len(citext)):
        pltext.append(citext[i] ^ key[(i+1) % len(key)])

    return pltext

def prepad(size):
    pre_pad = []
    nonce = 0
    for i in range(0, size, 16) :
        nonce +=1
        padding = nonce.to_bytes(16, 'little')
        pre_pad += padding
    return bytearray(pre_pad)

def aes_decrypt(citext, password):
    salt = b'SaltVb6CryptoAes'
    key = hashlib.pbkdf2_hmac('sha1', password, salt, 1000, dklen=32)
    aes_stream = prepad(len(citext))
    aes_stream.extend(citext)
    cipher = AES.new(key, AES.MODE_ECB)
    xor_key = cipher.encrypt(pad(aes_stream, 16))
    plaintext = bytearray(len(citext))
    for i in range(len(citext)) : plaintext[i] = xor_key[i] ^ citext[i]
    return plaintext

def aes_decrypt_str(citext, password):
    citext = bytearray.fromhex(citext.decode('utf-8'))
    citext = base64.b64decode(citext)
    return aes_decrypt(citext, password)

def get_str(addr):
    res = bytearray()
    length = 0
    data = idc.get_wide_word(addr+length)

    while data:
        res.append(data)
        length += 2
        data = idc.get_wide_word(addr+length)
    return res

def decrypt_all_strs(hex_func, decrypt_func, algo=0, patch=1):
    #List of addreses required manual provision
    citext_exception = []
    key_exception = []
    citext_addrs = []
    key_addrs = []
    strings = []

    for addr in idautils.XrefsTo(hex_func, flags=0):
        citext_addr = addr.frm
        while True:
              citext_addr = idc.prev_head(citext_addr)
              if idc.print_insn_mnem(citext_addr) == "mov" and idc.get_operand_type(citext_addr, 1) == 0x5 :
                  temp = idc.get_operand_value(citext_addr, 1)
                  if temp not in citext_exception:
                      citext_addrs.append(temp)
                  break

    for addr in idautils.XrefsTo(decrypt_func, flags=0):
        key_addr = addr.frm
        while True:
              key_addr = idc.prev_head(key_addr)   
              if idc.print_insn_mnem(key_addr) == "mov" and idc.get_operand_type(key_addr, 1) == 0x5 and idc.get_operand_value(key_addr, 0) == 0x2:
                  temp = idc.get_operand_value(key_addr, 1)
                  if temp not in key_exception:
                      key_addrs.append(temp)
                  break

    decrypted = []
    size = min(len(key_addrs), len(citext_addrs))
    citext_addrs = citext_addrs[:size]
    citext_addrs.extend(citext_exception)
    key_addrs = key_addrs[:size]
    key_addrs.extend(key_exception)

    for i in range(0, size+len(citext_exception)) :
        if citext_addrs[i] not in decrypted:
            decrypted.append(citext_addrs[i])
        else:
            continue

        print(f"{hex(citext_addrs[i])} {hex(key_addrs[i])}")
        if algo == 1:
            pltext = xor_decrypt_str(get_str(citext_addrs[i]), get_str(key_addrs[i]))
        elif algo == 2:
            pltext = rc4_decrypt_str(get_str(citext_addrs[i]), get_str(key_addrs[i]))
        else:
            pltext = aes_decrypt_str(get_str(citext_addrs[i]), get_str(key_addrs[i]))
        print(pltext)

        if pltext not in strings:
            idc.set_cmt(citext_addrs[i], pltext.decode('utf-8'), 1)
            strings.append(pltext)
            if patch:
                for idx in range(len(pltext)) :
                    idc.patch_word(citext_addrs[i] + idx*2, pltext[idx])
                    for pad_idx in range(idx + 1, idx*2) :
                        idc.patch_word(citext_addrs[i] + pad_idx*2, 0x00)
    return strings

''''
Please provide the address of the following functions
hex_func as Proc_1_3
decrypt_func as Proc_1_5

(void (__fastcall *)(char *, const wchar_t *))_vbaStrCopy)(
    v165,
    L"9FB61391D8974B3D8AD01F88F3CECED5B4E9100A3C10C6A37AC8670C078E23B9C0C7");
  v8 = Proc_1_3(v165);
  ((void (__fastcall *)(int *, int))_vbaStrMove)(&v162, v8);
  ((void (__fastcall *)(char *, const wchar_t *))_vbaStrCopy)(v163, L"OMSkahFpbDoSRbwObPrXoXrL");
  v120 = v162;
  v162 = 0;
  ((void (__fastcall *)(char *, int))_vbaStrMove)(v164, v120);
  v156 = Proc_1_5(v164, v163);

Please apply an IDC Script generated from http://sandsprite.com/vbdec/ to help fix up all functions
'''
hex_func =
decrypt_func =
strings = decrypt_all_strs(hex_func, decrypt_func, patch=0)

#Decrypt payload from resource file example
#citext = bytearray(open('CUSTOM101', 'rb').read())
#password = b'DDDJJFHHDII8387474765HHFNNFBGGFJJRKJKERJ439485TH8THTJMNBGJTIGH4I5YYIU45VBIUG4I7I1123405TY'
#open('payload.bin', 'wb').write(aes_decrypt(citext, password))
