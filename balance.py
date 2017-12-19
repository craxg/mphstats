#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime, timedelta
from operator import mul
import sys, traceback


# print "\033[H\033[J"

coins = {
    'monero': 'XMR',
    'electroneum': 'ETN',

    'zcash': 'ZEC',
    'zencash': 'XZC',
    'zclassic': 'ZCL',
    'bitcoin-gold': 'BTG',

    'ethereum': 'ETH',
    'ethereum-classic': 'ETC',
    'expanse': 'EXP',
    'musicoin': 'MUSIC',

    'groestlcoin': 'GRS',

    'maxcoin': 'MAX',

    'vertcoin': 'VTC',
    'monacoin': 'MONA',

    'zcoin': 'XZC',

    'myriadcoin-groestl': 'XMY',
    'digibyte-groestl': 'DGB',

    'feathercoin': 'FTC',

    'geocoin': 'GEO',
    'digibyte-qubit': 'DGB',
    'auroracoin-qubit': 'AUR',

    'litecoin': 'LTC',
    'gamecredits': 'GAME',
    'verge-scrypt': 'XVG',
    'sexcoin': 'SXC',

    'bitcoin-cash': 'BCH',
    'bitcoin': 'BTC',

    'siacoin': 'SC',

    'digibyte-skein': 'DGB',
    'myriadcoin-skein': 'XMY',

    'dash': 'DSH',
    'startcoin': 'START',
    'adzcoin': 'ADZ',

    'myriadcoin-yescrypt': 'XMY',
    'globalboosty': 'BSTY'
}
currencies = ['EUR', 'USD', 'ETH', 'BTC']
global_balances = {}


def get_currency_values():
    coin_list = ','.join([coins[coin] for coin in coins])
    response = requests.get(
        'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}'.format(coin_list, ','.join(currencies))
    )
    # response = type('test', (object,), {})()
    # response.text = '{"MONA":{"BTC":0.0007231,"EUR":11.28,"ETH":0.01898},"MAX":{"BTC":7.9e-7,"EUR":0.01232,"ETH":0.00002074},"ZEC":{"BTC":0.0284,"EUR":434.9,"ETH":0.7456},"EXP":{"BTC":0.00016,"EUR":2.5,"ETH":0.004201},"DSH":{"BTC":0.00000279,"EUR":0.04352,"ETH":0.00007325},"XVG":{"BTC":0.00000268,"EUR":0.0401,"ETH":0.00006809},"BSTY":{"BTC":0.00000177,"EUR":0.02761,"ETH":0.00004647},"LTC":{"BTC":0.01675,"EUR":261.39,"ETH":0.4396},"FTC":{"BTC":0.00002193,"EUR":0.3421,"ETH":0.0005757},"GAME":{"BTC":0.000148,"EUR":2.31,"ETH":0.003886},"XMY":{"BTC":4.6e-7,"EUR":0.007176,"ETH":0.00001208},"XZC":{"BTC":0.003259,"EUR":50.84,"ETH":0.08556},"MUSIC":{"BTC":0.00000159,"EUR":0.0248,"ETH":0.00004174},"DGB":{"BTC":0.0000019,"EUR":0.02964,"ETH":0.00004988},"BCH":{"BTC":0.09754,"EUR":1485.05,"ETH":2.56},"START":{"BTC":0.00000563,"EUR":0.08783,"ETH":0.0001478},"AUR":{"BTC":0.00008004,"EUR":1.25,"ETH":0.002101},"GRS":{"BTC":0.00007273,"EUR":1.13,"ETH":0.001909},"ETC":{"BTC":0.001809,"EUR":27.8,"ETH":0.04746},"VTC":{"BTC":0.000453,"EUR":7.07,"ETH":0.01189},"GEO":{"BTC":0.00009065,"EUR":1.41,"ETH":0.00238},"BTC":{"BTC":1,"EUR":15600.2,"ETH":26.25},"ZCL":{"BTC":0.0002283,"EUR":3.56,"ETH":0.005994},"SXC":{"BTC":0.00000551,"EUR":0.08596,"ETH":0.0001447},"BTG":{"BTC":0.01541,"EUR":240.4,"ETH":0.4046},"ETH":{"BTC":0.03809,"EUR":588.92,"ETH":1},"ETN":{"BTC":0.00000413,"EUR":0.06443,"ETH":0.0001084},"ADZ":{"BTC":0.00000199,"EUR":0.03104,"ETH":0.00005224},"XMR":{"BTC":0.01837,"EUR":279.91,"ETH":0.4823},"SC":{"BTC":8.3e-7,"EUR":0.01295,"ETH":0.00002179},"EUR":{"BTC":0.0000641,"EUR":1,"ETH":0.001698}}'
    return json.loads(response.text)


coin_values = get_currency_values()


def update_global_balances(pool, values):
    if pool not in global_balances:
        global_balances[pool] = {'BTC': 0, 'EUR': 0, 'USD': 0, 'ETH': 0}

    if pool != 'mph':
        values = {'BTC': values}

    for currency in ['BTC', 'EUR', 'ETH', 'USD']:
        for coin in values:
            if coin == currency:
                value = values[coin]
            else:
                value = values[coin] * float(coin_values[coin][currency])

            global_balances[pool][currency] += value


def get_mph_user_balances(api_key='1afc454ea54d7ff4f28d1ac27454e6a32f28143b3f974e4a893df3bd4f6d043c'):
    response = requests.get(
        'https://miningpoolhub.com/index.php?page=api&api_key={}&action=getuserallbalances'.format(api_key)
    )
    # response = type('test', (object,), {})()
    # response.text = '{"getuserallbalances":{"version":"1.0.0","runtime":3.8728713989258,"data":[{"coin":"litecoin","confirmed":1.656e-5,"unconfirmed":0,"ae_confirmed":0.00425096,"ae_unconfirmed":0,"exchange":0},{"coin":"maxcoin","confirmed":0.77474619,"unconfirmed":0,"ae_confirmed":0.34468033,"ae_unconfirmed":0,"exchange":0},{"coin":"groestlcoin","confirmed":0,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00409065,"exchange":0},{"coin":"vertcoin","confirmed":0,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00030975,"exchange":0},{"coin":"feathercoin","confirmed":0,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.20207995,"exchange":0.15672083},{"coin":"digibyte-skein","confirmed":0.98201473,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0,"exchange":1.5876169},{"coin":"ethereum","confirmed":0.00978967,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0,"exchange":0},{"coin":"globalboosty","confirmed":0,"unconfirmed":0.04461692,"ae_confirmed":0,"ae_unconfirmed":0,"exchange":0},{"coin":"siacoin","confirmed":0.12023824,"unconfirmed":0.15594542,"ae_confirmed":0,"ae_unconfirmed":0,"exchange":0},{"coin":"zcash","confirmed":0,"unconfirmed":0,"ae_confirmed":1.59e-5,"ae_unconfirmed":5.23e-5,"exchange":0.00050276},{"coin":"zclassic","confirmed":0.00470571,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00010567,"exchange":0.00058805},{"coin":"monero","confirmed":0,"unconfirmed":0,"ae_confirmed":7.622e-5,"ae_unconfirmed":0.00011162,"exchange":0.00046179},{"coin":"zcoin","confirmed":0.02633714,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.03389389,"exchange":0},{"coin":"monacoin","confirmed":0,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00302754,"exchange":0},{"coin":"zencash","confirmed":9.233e-5,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00267878,"exchange":0.00040137},{"coin":"bitcoin-gold","confirmed":0.00130727,"unconfirmed":0,"ae_confirmed":0,"ae_unconfirmed":0.00166712,"exchange":0.00022205}]}}'
    data = json.loads(response.text)['getuserallbalances']['data']
    values = {}
    # print(data)

    for item in data:
        # Get the coin symbol.
        coin = coins[item['coin']]

        # Sum up all the balances for the coin (auto exchanged, etc.)
        balance = sum([item[val] for val in item if isinstance(item[val], float)])

        # Check if the coin symbol already has a value.
        if coin in values:
            balance += values[coin]

        values[coin] = balance

    update_global_balances('mph', values)

    return values


def get_yii(pool, domain, key='total_earned'):
    response = requests.get('http://{}/api/wallet?address=13mfhuJ5PTu4FL1ph4ZYbJAxUpzmfxfzcY'.format(domain)).text
    data = json.loads(response)
    update_global_balances(pool, data[key])


def get_ahash_user_balances():
    get_yii('ahash', 'ahashpool.com')


def get_zpool_user_balances():
    get_yii('zpool', 'zpool.ca', 'total')


def output(pool='total'):
    global global_balances, currencies

    total = {'EUR': 0, 'BTC': 0, 'USD': 0, 'ETH': 0}

    for pool in sorted(global_balances):
        print("{}:".format(pool.upper()))
        for currency in currencies:
            value = global_balances[pool][currency]
            print("\t{}:\t{:.10f}".format(currency, value))
            total[currency] += value
        print("")

    print("TOTAL:")
    for currency in currencies:
        print("\t{}:\t{:.10f}".format(currency, total[currency]))
    print("")

    global_balances = {}


def main():
    try:
        get_mph_user_balances()
        get_ahash_user_balances()
        get_zpool_user_balances()

        output()
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno


if __name__ == "__main__":
    try:
        while True:
            stats = datetime.now()
            print "[{}] Stats fetched!".format(stats.strftime('%H:%M:%S'))
            main()
            stats += timedelta(seconds=900)
            print "Next status update: {}".format(stats.strftime('%H:%M:%S'))
            time.sleep(900)
    except KeyboardInterrupt:
        print "Exiting!"
        quit()
