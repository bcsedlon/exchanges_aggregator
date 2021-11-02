import ccxt

exchangeCoinbaseProSandbox = ccxt.coinbasepro({
    "apiKey": "3d08cf07a3dde17e2145a70f56b5cc6e",
    "secret": "ioV/v5StqGD1Lu2TQkXLUus4l5ZdrLyS+FTOXIyynp3+gILArjeu7YUT1rEcSK8zEJGgp7Uk2RkhRUSoIWRhNQ==",
    "password": "11fcplfjtyxl",
    "enableRateLimit": True
})

exchangeCoinbasePro = ccxt.coinbasepro({
    "apiKey": "",
    "secret": "",
    "password": "",
    "enableRateLimit": True
})

exchangeCoinbase = ccxt.coinbase({
    "apiKey": "",
    "secret": "",
    "enableRateLimit": True
})

exchangeCoinmate = ccxt.coinmate({
    "apiKey": "",
    "secret": "",
    "uid": "9",
    "enableRateLimit": True
})

exchangeHuobi = ccxt.huobi({
    "apiKey": "",
    "secret": "",
    "enableRateLimit": True
})

exchangeBinance = ccxt.binance({
    "apiKey": "",
    "secret": "",
    "enableRateLimit": True
})

exchanges = [exchangeBinance, exchangeHuobi, exchangeCoinmate, exchangeCoinbaseProSandbox]
#exchanges = [exchangeCoinbaseProSandbox]
