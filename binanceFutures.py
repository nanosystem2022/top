import json
import time
import ccxt
import random
import string

with open('config.json') as config_file:
    config = json.load(config_file)


if config['EXCHANGES']['BINANCE-FUTURES']['TESTNET']:
    exchange = ccxt.binance({
        'apiKey': config['EXCHANGES']['BINANCE-FUTURES']['API_KEY'],
        'secret': config['EXCHANGES']['BINANCE-FUTURES']['API_SECRET'],
        'options': {
            'defaultType': 'future',
        },
        'urls': {
            'api': {
                'public': 'https://testnet.binancefuture.com/fapi/v1',
                'private': 'https://testnet.binancefuture.com/fapi/v1',
            }, }
    })
    exchange.set_sandbox_mode(True)
else:
    exchange = ccxt.binance({
        'apiKey': config['EXCHANGES']['BINANCE-FUTURES']['API_KEY'],
        'secret': config['EXCHANGES']['BINANCE-FUTURES']['API_SECRET'],
        'options': {
            'defaultType': 'future',
        },
        'urls': {
            'api': {
                'public': 'https://fapi.binance.com/fapi/v1',
                'private': 'https://fapi.binance.com/fapi/v1',
            }, }
    })


class Bot:

    def __int__(self):
        pass

    def create_string(self):
        N = 7
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N))
        baseId = 'x-40PTWbMI'
        self.clientId = baseId + str(res)
        return

    def currency_check(self, symbol):
        if "USDT" in symbol:
            currency = symbol.replace("USDT", "/USDT")
        else:
            currency = symbol.replace("USD", "/USD")
        return currency
