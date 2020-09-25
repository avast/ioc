#!/usr/bin/python2.7

import socket,sys,time,logging




class easy_smarter():


	def __init__(self,  ip='192.168.4.1', port = 2081):
		self.ip = ip
		self.port = port
		self.sock = None

	def connect(self):
		# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.sock.settimeout(3)
			# connect the client
			self.sock.connect((self.ip, self.port))
			self.sock.settimeout(.5)    # 5 seconds. Set this after connecting.
			return True
		except Exception,e:
			logging.warning("Could not connect %s" %(str(e)))
			return False

	def read_data(self):
		resp = bytearray()
		timeout = 10
		while True:
			try:
				response = self.sock.recv(4096)
				resp.extend(bytearray(response))
				if resp[len(resp)-1]==0x7E:
					return resp
	 		except socket.timeout as exc:
				logging.warning('timed out waiting for data')	
			timeout -=1
			if timeout<=0:
				return bytearray()

	def send_command(self, indata, waitforresponse = True):
		self.sock.send(bytearray(indata))
		if waitforresponse:
			return self.read_data()
		else:
			return bytearray()

	def upload_firmware(self, filename, display = sys.stdout.write):
		fw = None
		total =0
		try:
			# try to open firmware file
			fw = open(filename,"rb")
			fw.seek(0,2)
			total = fw.tell()/256
			if (fw.tell()%256)>0:
				total+=1
			fw.seek(0)
		except Exception, e:
			logging.error("Could not load firmware from file %s ", str(e))
			return False
		
		display ("> Sending lead-in packet\n")
		self.send_command([0x6E, 0x7E], True)

		crc  = 0
		block =0
		result=0
		display ("> Starting update of %d blocks 256 bytes each\n" %(total))
		# read chunks of 256 bytes and construct a packet
		while True:
			retry = 5
        		chunk = bytearray(fw.read(256))
			if not chunk:
				break
	                #chunks are always of size of 256
			chunk.extend( bytearray([0]*(256-len(chunk))) )
			# now for each chunk compute 'CRC'
			for i in range(256):
				crc = (crc + chunk[i]) % 0xFFFFFFFF
 
        		# retry loop
		 	while True:
	        		size = len(chunk)
				packet = bytearray()
				packet.extend(bytearray([0x6f, block+1, (size>>8) & 0xff, (size) & 0xff, 0x7d]))
				packet.extend(chunk)
				packet.extend(bytearray([0x7e,0x7e,0x7e]))
			
				res = self.send_command(packet)

				# respond packet should always end like this
				result = 0
				if len(res)==3 and res[2]==0x7E:
					major = res[0]
	        	                if major==3:
						result = res[1]
					else:
						result = res[0]<<4 & res[1]

				if result!=1:		
					retry-=1
					if retry>0:
						time.sleep(1)
						continue		
					display("\nError writing page no. %d\n" % (block+1))
					break
#                                  
				if  block%4==0 and result==1:
					display(".")
				if result==1:
					break
				#sys.stdout.write("sending page %d of %d   " %(block+1, total))
			if result!=1:
				break
			block +=1

		print "\n"
		if result==1:
			time.sleep(1)
			# sending CRC and closing block
			res = self.send_command([0x70, (crc>>24) & 0xFF, (crc>>16) & 0xFF,(crc>>8) & 0xFF,  crc & 0xFF, 0x7E], True)
			


			if len(res)==3 and res[2]==0x7E:
				major = res[0]
	                	if major==3:
					result = res[1]
				else:
					result = res[0]<<4 & res[1]
			if result==1:
				display("\nUpdate complete!\n")
			else:
				display ("\nError finishing firmware %d.\n" % (result))
		else:
			display ("\nError writing firmware %d.\n" %(result))
		return result
		

	def disconnect(self):
		self.sock.close()