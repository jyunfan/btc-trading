import logging

from exchange import Exchange
from bitstamp import client

logger = logging.getLogger( __name__ )

class Bitstamp(Exchange):
    def __init__(self, keyfile):
        f = open(keyfile)
        keys = f.readlines()
        f.close()
        if len(keys) != 3:
            logger.error("Incorrect key file")
            exit()

        [user, key, secret] = [keys[0].strip(), keys[1].strip(), keys[2].strip()]
        self.bs_client = client.trading(username=user, key=key, secret=secret)
        self.bs_client_public = client.public()


    def balance(self):
        # {u'btc_reserved': 1.0, u'fee': 0.25, u'btc_available': 18.00767799, u'usd_reserved': 0.0, u'btc_balance': 19.00767799, u'usd_balance': 399.0, u'usd_available': 399.0}
        balance = self.bs_client.account_balance()

        # Convert string to double
        for attr in balance:
            balance[attr] = float(balance[attr])
        return balance


    def ticker(self):
        # example: {u'volume': u'40457.80751208', u'last': u'384.02', u'timestamp': u'1446878501', u'bid': u'384.02', u'vwap': u'378.59', u'high': u'396.67', u'low': u'362.64', u'ask': u'385.90', u'open': 374.41}
        tick = self.bs_client_public.ticker()
        for attr in tick:
            tick[attr] = float(tick[attr])
        return tick


    def open_orders(self):
        orders = self.bs_client.open_orders()
        return orders


    def buy(self, amount, price):
        result = self.bs_client.buy_limit_order(amount=amount, price=price)
        print("buy", result)


    def sell(self, amount, price):
        result = self.bs_client.sell_limit_order(amount=amount, price=price)
        print("sell", result);


    def cancel_order(self, order_id):
        self.bs_client.cancel_order(order_id)


    def cancel_all_orders(self, coin):
        # coin is 'btc' or 'ltc', but unused now
        orders = self.open_orders()
        for order in orders:
            self.bs_client.cancel_order(order['id'])
