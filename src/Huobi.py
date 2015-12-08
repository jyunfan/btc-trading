#coding=utf-8

import logging

import sys
from exchange import Exchange
import huobi_api

logger = logging.getLogger( __name__ )

def cointype(coin):
    if coin == 'btc':
        return 1
    elif coin == 'ltc':
        return 2
    else:
        raise ValueError()


class Huobi(Exchange):
    def __init__(self, keyfile):
        f = open(keyfile)
        keys = f.readlines()
        f.close()
        if len(keys) != 4:
            logger.error("Incorrect key file")
            sys.exit(1)

        [user, key, secret, trade_pass] = [keys[0].strip(), keys[1].strip(), keys[2].strip(), keys[3].strip()]
        #self.client = HuobiClient.trading(key=key, secret=secret)
        huobi_api.ACCESS_KEY = key
        huobi_api.SECRET_KEY = secret
        huobi_api.TRADE_PASS = trade_pass


    def balance(self):
        # {u'btc_reserved': 1.0, u'fee': 0.25, u'btc_available': 18.00767799, u'usd_reserved': 0.0, u'btc_balance': 19.00767799, u'usd_balance': 399.0, u'usd_available': 399.0}
        info = huobi_api.getAccountInfo()

        # Convert string to double
        ret = {'btc_balance':float(info['available_btc_display']) +
                             float(info['frozen_btc_display']),
               'cny_balance':float(info['available_cny_display']) +
                             float(info['frozen_cny_display']),
                }
        return ret


    def ticker(self):
        # example: {u'volume': u'40457.80751208', u'last': u'384.02', u'timestamp': u'1446878501', u'bid': u'384.02', u'vwap': u'378.59', u'high': u'396.67', u'low': u'362.64', u'ask': u'385.90', u'open': 374.41}
        coin = 'btc'
        tick = huobi_api.ticker(coin)
        return tick


    def open_orders(self, coin):
        orders = huobi_api.getNewDealOrders(cointype(coin), 'get_orders')
        return orders


    def buy(self, amount, price, coin='btc'):
        result = huobi_api.buy(coinType=cointype(coin),price=price,amount=amount,tradePassword=huobi_api.TRADE_PASS,tradeid=None,method='buy')
        print("buy", result)


    def sell(self, amount, price, coin='btc'):
        result = huobi_api.sell(coinType=cointype(coin),price=price,amount=amount,tradePassword=huobi_api.TRADE_PASS,tradeid=None,method='sell')
        print("sell", result)


    def cancel_order(self, order_id, coin):
        huobi_api.cancelOrder(cointype(coin), order_id, 'cancel_order')


    def cancel_all_orders(self, coin='btc'):
        print('get orders')
        orders = self.open_orders(coin)
        print('cancel all orders')
        for order in orders:
            self.cancel_order(order['id'], coin)
