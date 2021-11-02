# -*- coding: utf-8 -*-

import os
import sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt
import json
import csv
import logging
logging.basicConfig(handlers=[logging.FileHandler(filename="log.txt", encoding='utf-8', mode='w')],
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.ERROR)

try:
    from exchanges_private import exchanges
except:
    print('Rename exchanges_example.py to exchanges_private.py and fill credentials!')
    exit()

#from exchanges_example import exchanges

#x = [i for i, a in locals().items() if a == exchange][0]
#print(x)

param_key = ''
param_value = ''

# burza, datum, par (fiat-jina mena), zmena fiat, zmena druheho coinu
header = ['exchange', 'datetime', 'symbol', 'cost', 'amount', 'side']
f = open('export.csv', 'w',  encoding='UTF8', newline='')
writer = csv.writer(f, delimiter=';')
writer.writerow(header)

for exchange in exchanges:
    allMyTrades = []

    print(exchange.name)

    symbol = None
    if exchange.name.find('Coinbase') >= 0:
        symbol = 'BTC/USD'
        exchange.set_sandbox_mode(True)

    print(exchange.requiredCredentials)  # prints required credentials
    exchange.checkRequiredCredentials()  # raises AuthenticationError

    try:
        balance = exchange.fetch_balance()
        print(json.dumps(balance, indent=3, sort_keys=True))
    except Exception as exception:
        logging.exception(exchange.name)
        continue

    while True:

        myTrades = exchange.fetch_my_trades(symbol=symbol, since=None, params={param_key: param_value})

        if exchange.last_response_headers._store.get('cb-after'):
            param_key = 'after'
            param_value = exchange.last_response_headers._store['cb-after'][1]
            allMyTrades.extend(myTrades)
        else:
            allMyTrades.extend(myTrades)
            break

    for trade in allMyTrades:
        #print(json.dumps(trade, indent=3, sort_keys=True))
        data = list()
        data.append(exchange.name)
        data.append(trade['datetime'])
        data.append(trade['symbol'])
        data.append(trade['cost'])
        data.append(trade['amount'])
        data.append(trade['side'])
        writer.writerow(data)

f.close()