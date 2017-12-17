#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime, timedelta


symbols = {
	"adzcoin": "ADZ",
	"auroracoin": "AUR",
	"bitcoin": "BTC",
	"bitcoin-cash": "BCH",
	"bitcoin-gold": "BTG",
	"dash": "DSH",
	"digibyte": "DGB",
	"digibyte-groestl": "DGB",
	"digibyte-skein": "DGB",
	"digibyte-qubit": "DGB",
	"ethereum": "ETH",
	"ethereum-classic": "ETC",
	"expanse": "EXP",
	"feathercoin": "FTC",
	"gamecredits": "GAME",
	"geocoin": "GEO",
	"globalboosty": "BSTY",
	"groestlcoin": "GRS",
	"litecoin": "LTC",
	"maxcoin": "MAX",
	"monacoin": "MONA",
	"monero": "XMR",
	"musicoin": "MUSIC",
	"myriadcoin": "XMY",
	"myriadcoin-skein": "XMY",
	"myriadcoin-groestl": "XMY",
	"myriadcoin-yescrypt": "XMY",
	"sexcoin": "SXC",
	"siacoin": "SC",
	"startcoin": "START",
	"verge": "XVG",
	"vertcoin": "VTC",
	"zcash": "ZEC",
	"zclassic": "ZCL",
	"zcoin": "XZC",
	"zencash": "ZEN"
}

def main():

	# Query the MPH API to get all current balances
	url = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key=1afc454ea54d7ff4f28d1ac27454e6a32f28143b3f974e4a893df3bd4f6d043c"
	raw_response = requests.get(url).text
	response = json.loads(raw_response)

	# Parse the response into a basic dictionary keyed on coin name
	coins = {}
	for coin in response["getuserallbalances"]["data"]:
		symbol = symbols[coin["coin"]]
		balance = sum([
			coin["confirmed"],
			coin["unconfirmed"],
			coin["ae_confirmed"],
			coin["ae_unconfirmed"],
			coin["exchange"]
		 ])
		coins[symbol] = balance

	lcoins = ','.join([coin for coin in coins])
	url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={},EUR,BTC,ETH&tsyms=BTC,EUR,ETH'.format(lcoins)
	raw = requests.get(url).text
	#raw = '{"DGB":{"BTC":0.00000115,"EUR":0.01717,"ETH":0.00002984},"ZEC":{"BTC":0.02593,"EUR":381.91,"ETH":0.6728},"VTC":{"BTC":0.0004318,"EUR":6.45,"ETH":0.0112},"MONA":{"BTC":0.0008006,"EUR":11.96,"ETH":0.02077},"ZCL":{"BTC":0.0002156,"EUR":3.22,"ETH":0.005594},"MAX":{"BTC":7.7e-7,"EUR":0.0115,"ETH":0.00001998},"ZEN":{"BTC":0.001836,"EUR":27.42,"ETH":0.04764},"BTG":{"BTC":0.0161,"EUR":240.42,"ETH":0.4177},"LTC":{"BTC":0.01747,"EUR":261.41,"ETH":0.4551},"FTC":{"BTC":0.00002652,"EUR":0.396,"ETH":0.0006881},"MUSIC":{"BTC":0.00000137,"EUR":0.02046,"ETH":0.00003555},"XZC":{"BTC":0.003154,"EUR":47.1,"ETH":0.08184},"SC":{"BTC":6.1e-7,"EUR":0.009109,"ETH":0.00001583},"ETH":{"BTC":0.03854,"EUR":572.68,"ETH":1},"XMR":{"BTC":0.01757,"EUR":258.34,"ETH":0.4559}}'
	data = json.loads(raw)
	ahash = requests.get('http://www.ahashpool.com/api/wallet?address=13mfhuJ5PTu4FL1ph4ZYbJAxUpzmfxfzcY').text
	ahash = json.loads(ahash)
	zpool = requests.get('http://zpool.ca/api/wallet?address=13mfhuJ5PTu4FL1ph4ZYbJAxUpzmfxfzcY').text
	zpool = json.loads(zpool)

        btc_total = float(ahash['total_earned']) + float(zpool['total'])
	eur_balance = 0
	eth_balance = 0
	btc_balance = btc_total
	final = {'eur':0, 'eth':0, 'btc': 0}

	for coin in data:
                if coin != 'ETH' and coin != 'EUR' and coin != 'BTC':
                        btc = data[coin]['BTC']
                        eur = data[coin]['EUR']
                        eth = data[coin]['ETH']
                        val = float(coins[coin])
                        x = {}
                        x['eur'] = val * float(eur)
                        x['eth'] = val * float(eth)
                        x['btc'] = val * float(btc)

                        #if coin != 'ETH' and coin != 'EUR' and coin != 'BTC':
                        eur_balance += x['eur']
                        eth_balance += x['eth']
                        btc_balance += x['btc']
                        

		#print("|-------------------------------------")
		#print("| {}:".format(coin))
		#print("|        EUR: {:.10f}".format(x['eur']))
		#print("|        ETH: {:.10f}".format(x['eth']))
		#print("|        BTC: {:.10f}".format(x['btc']))

        final['eur'] += btc_total * float(data['EUR']['BTC'])
        final['eth'] += btc_total * float(data['ETH']['BTC'])
        final['btc'] += btc_total

        if 'ETH' in coins:
                val = float(coins['ETH'])
                final['eur'] += val * float(data['ETH']['EUR'])
                final['btc'] += val * float(data['ETH']['BTC'])
                final['eth'] + val
        
        #final = {'eth': btc_total * float(eth), 'eur': btc_total * float(eur), 'btc': btc_total}

        #final = coins['ETH']
	curtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	
	print "[{}] unexchanged balance: EUR: {:.10f}  | ETH: {:.10f} | BTC: {:.10f}".format(curtime, eur_balance, eth_balance, btc_balance)
	print "[{}]   exchanged balance: EUR: {:.10f}  | ETH: {:.10f} | BTC: {:.10f}".format(curtime, final['eur'], final['eth'], final['btc'])
	print "[{}]       total balance: EUR: {:.10f} | ETH: {:.10f} | BTC: {:.10f}".format(curtime, eur_balance + final['eur'], eth_balance + final['eth'], btc_balance + final['btc'])

	if final['eth'] > 0.01:
                print "You've reached the minimum payout threshold."

	#print("|-------------------------------------")
	#print("| TOTALS:")
	#print("|        EUR: {:.10f}".format(eur_balance))
	#print("|        ETH: {:.10f}".format(eth_balance))
	#print("|        BTC: {:.10f}".format(btc_balance))
	#print("|-------------------------------------")


if __name__ == "__main__":
        try:
                while True:
                        main()
                        stats = datetime.now() + timedelta(seconds=900)
                        print "--> Next stats at: {}".format(stats.strftime('%H:%M:%S'))
                        time.sleep(900)
        except KeyboardInterrupt:
                print "Exiting!"
                quit()
