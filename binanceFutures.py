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

    def run(self, data):
        print(data['close_position'])
        if data['close_position'] == 'True':
            print("Closing Position")
            self.close_position(symbol=data['symbol'])
        else:
            if 'cancel_orders' in data:
                print("Cancelling Order")
                exchange.cancel_all_orders(symbol=data['symbol'])
            if 'type' in data:
                print("Placing Order")
                if 'price' in data:
                    price = data['price']
                else:
                    price = 0

                if data['order_mode'] == 'Both':
                    take_profit_percent = float(data['take_profit_percent']) / 100
                    stop_loss_percent = float(data['stop_loss_percent']) / 100
                    current_price = exchange.fetch_ticker(data['symbol'])['last']
                    if data['side'].capitalize() == 'Buy':
                        take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent),
                                                  2)
                        stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                    elif data['side'].capitalize() == 'Sell':
                        take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent),
                                                  2)
                        stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)

                    print("Take Profit Price: " + str(take_profit_price))
                    print("Stop Loss Price: " + str(stop_loss_price))

                    self.create_string()
                    params = {
                        "newClientOrderId": self.clientId,
                        'reduceOnly': False
                    }
                    if data['type'] == 'Limit':
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              price=float(price), params=params)
                    else:
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              params=params)

                    self.set_risk(data['symbol'], data, stop_loss_price, take_profit_price)


                elif data['order_mode'] == 'Profit':
                    take_profit_percent = float(data['take_profit_percent']) / 100
                    current_price = exchange.fetch_ticker(data['symbol'])['last']

                    if data['side'].capitalize() == 'Buy':
                        take_profit_price = round(float(current_price) + (float(current_price) * take_profit_percent),
                                                  2)
                    elif data['side'].capitalize() == 'Sell':
                        take_profit_price = round(float(current_price) - (float(current_price) * take_profit_percent),
                                                  2)

                    print("Take Profit Price: " + str(take_profit_price))

                    self.create_string()
                    params = {
                        "newClientOrderId": self.clientId,
                        'reduceOnly': False
                    }

                    if data['type'] == 'Limit':
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              price=float(price), params=params)
                    else:
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              params=params)

                    self.set_risk(data['symbol'], data, 0, take_profit_price)


                elif data['order_mode'] == 'Stop':
                    stop_loss_percent = float(data['stop_loss_percent']) / 100
                    current_price = exchange.fetch_ticker(data['symbol'])['last']

                    if data['side'].capitalize() == 'Buy':
                        stop_loss_price = round(float(current_price) - (float(current_price) * stop_loss_percent), 2)
                    elif data['side'].capitalize() == 'Sell':
                        stop_loss_price = round(float(current_price) + (float(current_price) * stop_loss_percent), 2)

                    print("Stop Loss Price: " + str(stop_loss_price))

                    self.create_string()
                    params = {
                        "newClientOrderId": self.clientId,
                        'reduceOnly': False
                    }

                    if data['type'] == 'Limit':
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              price=float(price), params=params)
                    else:
                        exchange.create_order(data['symbol'], data['type'], data['side'].capitalize(), float(data['qty']),
                                              params=params)

                    self.set_risk(data['symbol'], data, stop_loss_price, 0)

                else:
                    return {
                        'status': 'error'
                    }
