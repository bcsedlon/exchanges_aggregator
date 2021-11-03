# -*- coding: utf-8 -*-

import os
import sys
import getopt
import datetime

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
#sys.tracebacklimit = 0

import ccxt
import json
import csv
import logging
import importlib

logging.basicConfig(handlers=[logging.FileHandler(filename="log.txt", encoding='utf-8', mode='w')],
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S',
                    level=logging.ERROR)


def main(argv):

    outputFileName = 'export.csv'
    dateFrom = datetime.date.today().replace(day=1).strftime("%Y-%m-%d")
    #dateFrom = '2021-10-01'

    dateTo = datetime.date.today().strftime("%Y-%m-%d")
    exchangesFileName = 'exchanges_private.py'

    try:
        opts, args = getopt.getopt(argv, 'he:f:t:o:l',
                                   ['exchangesFileName=', 'dateFrom=', 'dateTo=', 'outputFileName='])
    except getopt.GetoptError as e:
        print(e)
        print('run.py -e <exchangesfile> -f <datefrom> -t <dateto> -o <outputfile> -l(log)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -e <exchangesfile> -f <datefrom> -t <dateto> -o <outputfile> -l(log)')
            sys.exit()
        elif opt in ("-e"):
            exchangesFileName = arg
        elif opt in ("-f"):
            dateFrom = arg
        elif opt in ("-t"):
            dateTo = arg
        elif opt in ("-o"):
            outputFileName = arg
        elif opt in ("-l"):
            log = True

    if not os.path.exists(exchangesFileName):
        #print('Rename exchanges_example.py to exchanges_private.py and fill credentials!')
        print('Exchanges file {} not exists!'.format(exchangesFileName))
        exit()

    dateFrom = datetime.datetime.strptime(dateFrom, '%Y-%m-%d')
    dateTo = datetime.datetime.strptime(dateTo, '%Y-%m-%d')
    print('Date range from {} to {}'.format(dateFrom.strftime('%Y-%m-%d'), dateTo.strftime('%Y-%m-%d')))
    dateFrom = int(dateFrom.timestamp()) * 1000
    dateTo = int(dateTo.timestamp() + 24 * 60 * 60) * 1000
    #huobi https://github.com/ccxt/ccxt/issues/6512

    exchangesFileName = (os.path.splitext(exchangesFileName)[0])
    exchangesModule = importlib.import_module(exchangesFileName)
    exchanges = exchangesModule.exchanges
    #from exchanges_private import exchanges

    # x = [i for i, a in locals().items() if a == exchange][0]
    # print(x)

    param_key = ''
    param_value = ''

    # burza, datum, par (fiat-jina mena), zmena fiat, zmena druheho coinu
    header = ['exchange', 'datetime', 'symbol', 'cost', 'amount', 'side']
    f = open(outputFileName, 'w', encoding='UTF8', newline='')
    writer = csv.writer(f, delimiter=';')
    writer.writerow(header)

    for exchange in exchanges:
        allMyTrades = []

        print(exchange.name)

        try:
            if exchange.sandbox:
                print('Set sandbox mode')
                exchange.set_sandbox_mode(exchange.sandbox)
        except:
            pass

        symbols = []
        if exchange.name.find('Coinbase') >= 0:
            # symbol = 'BTC/USD'
            markets = exchange.load_markets()
            symbols.extend(markets)
            # print(json.dumps(markets, indent=3, sort_keys=True))
            #for market in markets:
            #   print(market)
        else:
            symbols.append(None)

        params = {param_key: param_value}
        if exchange.name.find('Huobi') >= 0:
            #dateTo = ccxt.huobi.parse8601(dateTo)  # +2 days allowed range
            param = {
                'end-date': dateTo  # yyyy-mm-dd format
            }
            params.update(param)

        #print(exchange.requiredCredentials)  # prints required credentials
        exchange.checkRequiredCredentials()  # raises AuthenticationError

        try:
            balance = exchange.fetch_balance()
            #print(json.dumps(balance, indent=3, sort_keys=True))
        except Exception as exception:
            logging.error(exchange.name, )
            logging.error(repr(exception))
            logging.exception(exception)
            print(repr(exception))
            print('ERROR')
            continue

        for symbol in symbols:
            while True:
                #if symbol != None:
                #    print(symbol)

                myTrades = exchange.fetch_my_trades(symbol=symbol, since=dateFrom, params=params)  #{param_key: param_value})
                #if len(myTrades) == 0:
                #    break

                if exchange.last_response_headers._store.get('cb-after'):
                    param_key = 'after'
                    param_value = exchange.last_response_headers._store['cb-after'][1]
                    params.update({param_key: param_value})
                    allMyTrades.extend(myTrades)
                else:
                    allMyTrades.extend(myTrades)
                    break

                if len(myTrades) > 0:
                    trade = myTrades[-1]
                    if trade['timestamp'] >= dateTo:
                        break


        for trade in allMyTrades:
            # print(json.dumps(trade, indent=3, sort_keys=True))
            if trade['timestamp'] >= dateTo:
                break

            data = list()
            data.append(exchange.name)
            data.append(trade['datetime'])
            data.append(trade['symbol'])
            data.append(trade['cost'])
            data.append(trade['amount'])
            data.append(trade['side'])
            writer.writerow(data)

        print('OK')

    f.close()
    print('Done, see {}'.format(outputFileName))


if __name__ == "__main__":
    main(sys.argv[1:])
