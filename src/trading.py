#!/usr/bin/python

import sys
import logging
from time import sleep

# https://github.com/kmadac/bitstamp-python-client.git
import bitstamp.client

import price

LOOP_INTERVAL = 60

logger = logging.getLogger( __name__ )

""" Decide whether should buy or sell by using short and long term average. """
def decide_action():
#    window_short =  180 # 3 hours
#    window_long  = 2160 # 3 days
    window_short =  60 #  1 hour
    window_long  = 720 # 12 hours
    p = price.get_current_price([window_short, window_long])

    logger.debug("short SMA = %.2f, long SMA = %.2f" % (p[0], p[1]))

    if p[0] > p[1]:
        return "buy"
    else:
        return "sell"

class exchange():
    BTC_MAX = 3

    def __init__(self, keyfile):
        f = open(keyfile)
        keys = f.readlines()
        f.close()
        if len(keys) != 3:
            logger.error("Incorrect key file")
            exit()

        [user, key, secret] = [keys[0].strip(), keys[1].strip(), keys[2].strip()]
        self.bs_client = bitstamp.client.trading(username=user, key=key, secret=secret)
        self.bs_client_public = bitstamp.client.public()

    def get_balance(self):
        balance = self.bs_client.account_balance()

        # Convert string to double
        for attr in balance:
            balance[attr] = float(balance[attr])
        return balance

    def cancel_all(self):
        logger.debug("cancel_all()")

        orders = self.bs_client.open_orders()
        for order in orders:
            logger.info('Cancel order %s' % order['id'])
            self.bs_client.cancel_order(order['id'])

    def buy(self):
        self.cancel_all()

        # Get current ask
        ticker = self.bs_client_public.ticker()
        for attr in ticker:
            ticker[attr] = float(ticker[attr])
        ask = ticker['ask']
        price = ask * 1.01
        logger.info('ask = %.2f' % ask)

        balance = self.get_balance()
        btc_to_buy = (balance['usd_available'] / price) * 0.99

        if balance['usd_available'] < 100:
            logger.info('USD available = %.2f, skip buy' % balance['usd_available'])
            return

        btc_to_buy = '%.2f' % min(btc_to_buy, self.BTC_MAX)
        price = '%.2f' % price
        logger.info('Buy %s BTC at %s USD' % (btc_to_buy, price))
        response = self.bs_client.buy_limit_order(amount=btc_to_buy, price=price)
        logger.info('Response of buy: id=%(id)s, amount=%(amount)s, price=%(price)s, datetime=%(datetime)s' % response)

    def sell(self):
        logger.debug("sell()")

        self.cancel_all()

        ticker = self.bs_client_public.ticker()
        for attr in ticker:
            logger.debug("ticker[%s] = %s" % (attr, ticker[attr]))
            ticker[attr] = float(ticker[attr])
        bid = ticker['bid']
        price = bid * 0.99
        logger.info('bid = %.2f' % bid)

        balance = self.get_balance()
        btc_to_sell = balance['btc_available'] * 0.99

        logger.info(btc_to_sell)
        if btc_to_sell < 1:
            logger.info('BTC available = %.2f, skip sell' % btc_to_sell)
            return

        btc_to_sell = '%.2f' % min(btc_to_sell, self.BTC_MAX)
        price = '%.2f' % price
        logger.info('Sell %s BTC at %s USD' % (btc_to_sell, price))
        response = self.bs_client.sell_limit_order(amount=btc_to_sell, price=price)
        logger.info('Response of sell: id=%(id)s, amount=%(amount)s, price=%(price)s, datetime=%(datetime)s' % response)

def trading_loop():
    action = decide_action()
    ex = exchange(sys.argv[1])
    for i in range(18):
        print "iteration %d" % i
#        try:
        if action == 'buy':
            ex.buy()
        else:
            ex.sell()
#        except:
#            print sys.exc_info()[0]
#            logger.error("Unknwon exception in main loop")
#        finally:
        sleep(LOOP_INTERVAL)

def main():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup Handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    # Setup Logger
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    trading_loop()

if __name__ == "__main__":
    main()
