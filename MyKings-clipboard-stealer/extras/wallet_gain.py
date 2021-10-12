#!/usr/bin/python3


"""
Script for querying information about how muh crypto money wallets received
Data received should be in a json format where wallet addresses are objects containing information
about them. Information must contain "currency" with a correct tag, because script queries only
one API based on that tag. The "currency" is a list in a case when one address may belong to multiple
cryptocurrencies

Example input:
{
	"wallet_address" :
	{
		"currency": ["Bitcoin"],
		"samples": [sha1, sha2, sha3, sha4],
		"any_other_info" : "useful information"
	},
	"wallet_address2" :
	{
		"currency": ["Ethereum"]
	}
}
"""


import argparse
import os
import json
import requests
import time
import datetime
from tqdm import tqdm


UPDATE_INTERVAL = 1		#Number of days for which info will not be updated
COIN_VALUES = { 'ReddCoin' : 0.00245}	#Dict of crypto worth in dollars (USD)
#----------------------------------------------------------
def api_delay(api: str):
	"""
	Delays for different APIs to avoid exceeding quotas
	"""
	delays = {
		'Bitcoin' : 2,
		'prices' : 1,
		'Ethereum' : 1,
		'Dogecoin' : 1,
		'ReddCoin' : 1,
		'default' : 0,
	}
	if api in delays:
		time.sleep(delays[api])
	else:
		time.sleep(delays['default'])

#----------------------------------------------------------
def get_price(curr: str):
	"""
	Get price of cryptocurrency curr. It is recommended to check success of this operation.
	For more unusual crypto currencies raise the limit in url.
	"""
	if curr in COIN_VALUES:
		return

	api_delay('prices')
	resp = requests.get("https://api.coinstats.app/public/v1/coins?skip=0&limit=20&currency=USD")
	if resp.status_code == 200:
		info = json.loads(resp.text)['coins']
		for x in info:
			if x['name'] == curr:
				COIN_VALUES[curr] = x['price']
	else:
		print(f'Failed to get price of {curr}')
#----------------------------------------------------------
def get_ReddCoin_info(wallet: str, info: dict):
	"""
	Get information about wallet. It is expected that in COIN_VALUES is value of this cryptocurrency
	Functions receives wallet address and actual information - dictionary.
	Function returns original information with these added/updated keys:
		- 'received' => how much crypto wallet received
		- 'received_dollars' => What amount of USD is worth the crypto in 'received'
		- 'updated' => date and time when was info updated (to avoid updating recently updated wallets)
	"""
	resp = requests.get('https://live.reddcoin.com/api/addr/' + wallet)
	if resp.status_code == 200:
		response = json.loads(resp.text)
		info['received'] = float(response['totalReceived'])
		info['received_dollars'] = info['received'] * COIN_VALUES['ReddCoin']
		info['updated'] = datetime.datetime.now().isoformat()
	return info
#----------------------------------------------------------
def get_Dogecoin_info(wallet: str, info: dict):
	"""
	Get information about wallet. It is expected that in COIN_VALUES is value of this cryptocurrency
	Functions receives wallet address and actual information - dictionary.
	Function returns original information with these added/updated keys:
		- 'received' => how much crypto wallet received
		- 'received_dollars' => What amount of USD is worth the crypto in 'received'
		- 'updated' => date and time when was info updated (to avoid updating recently updated wallets)
	"""
	resp = requests.get('https://dogechain.info/api/v1/address/received/' + wallet)
	if resp.status_code == 200:
		response = json.loads(resp.text)
		if response['success'] == 1:
			info['received'] = float(response['received'])
			info['received_dollars'] = info['received'] * COIN_VALUES['Dogecoin']
			info['updated'] = datetime.datetime.now().isoformat()
	return info
#----------------------------------------------------------
def get_Ethereum_info(wallet: str, info: dict):
	"""
	Get information about wallet. It is expected that in COIN_VALUES is value of this cryptocurrency
	Functions receives wallet address and actual information - dictionary.
	Function returns original information with these added/updated keys:
		- 'received' => how much crypto wallet received
		- 'received_dollars' => What amount of USD is worth the crypto in 'received'
		- 'updated' => date and time when was info updated (to avoid updating recently updated wallets)
	"""
	resp = requests.get('https://api.blockcypher.com/v1/eth/main/addrs/' + wallet)
	if resp.status_code == 200:
		response = json.loads(resp.text)
		info['received'] = response['total_received'] / 10**18
		info['received_dollars'] = info['received'] * COIN_VALUES['Ethereum']
		info['updated'] = datetime.datetime.now().isoformat()
	return info
#----------------------------------------------------------
def get_Bitcoin_info(wallet: str, info: dict):
	"""
	Get information about wallet. It is expected that in COIN_VALUES is value of this cryptocurrency
	Functions receives wallet address and actual information - dictionary.
	Function returns original information with these added/updated keys:
		- 'received' => how much crypto wallet received
		- 'received_dollars' => What amount of USD is worth the crypto in 'received'
		- 'updated' => date and time when was info updated (to avoid updating recently updated wallets)
	"""
	resp = requests.get('https://blockchain.info/q/getreceivedbyaddress/' + wallet)
	if resp.status_code == 200:
		info['received'] = int(resp.text) / 10**8
		info['received_dollars'] = info['received'] * COIN_VALUES['Bitcoin']
		info['updated'] = datetime.datetime.now().isoformat()
	return info
#----------------------------------------------------------
def get_wallet_info(wallet: str, info: dict):
	"""
	Receives wallet and information about that wallet. If the cryptocurrency is one of
	Bitcoin/Ethereum/Dogecoin/ReddCoin function fills information about wallet with
	amounts of crypto received.
	Function returns original information with these added/updated keys:
		- 'received' => how much crypto wallet received
		- 'received_dollars' => What amount of USD is worth the crypto in 'received'
		- 'updated' => date and time when was info updated (to avoid updating recently updated wallets)
	"""
	#return if updated recently
	if 'updated' in info:
		if datetime.datetime.fromisoformat(info['updated']) + datetime.timedelta(days = UPDATE_INTERVAL) > datetime.datetime.now():
			return info

	#get the amount of money received to the wallet
	#these wallets won't have collisions in tags, so it is save to overwrite old amounts
	api_delay(info['currency'][0])
	if 'Bitcoin' in info['currency']:
		get_price('Bitcoin')
		info = get_Bitcoin_info(wallet, info)
	if 'Ethereum' in info['currency']:
		get_price('Ethereum')
		info = get_Ethereum_info(wallet, info)
	if 'Dogecoin' in info['currency']:
		get_price('Dogecoin')
		info = get_Dogecoin_info(wallet, info)
	if 'ReddCoin' in info['currency']:
		get_price('ReddCoin')
		info = get_ReddCoin_info(wallet, info)
	return info
#----------------------------------------------------------
def main():

	argparser = argparse.ArgumentParser()
	argparser.add_argument('--infile', '-if', required = True, help = 'json file with wallets')
	argparser.add_argument('--outfile', '-of', required = False, help = 'json to save wallets with new information')
	args = argparser.parse_args()

	if not os.path.exists(args.infile):
		print('Input file does not exist...')
		exit()

	with open(args.infile, 'rb') as f:
		data = json.load(f)

	#iterate through wallets and information
	for wallet, info in tqdm(data.items()):
		#query information
		data[wallet] = get_wallet_info(wallet, info)

	#return results - save to file or just print if outfile is not specified
	if args.outfile:
		with open(args.outfile, 'w') as f:
			json.dump(data, f)
	else:
		print(data)
#----------------------------------------------------------
if __name__ == '__main__':
	main()
