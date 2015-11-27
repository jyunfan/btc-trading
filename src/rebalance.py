""" Rebalance cash and BTC
"""

import time
import logging
from datetime import datetime
from Bitstamp import Bitstamp

FORMAT = '%(asctime)-15s %(module)s %(message)s'
logging.basicConfig(level=logging.INFO, filename='rebalance.log', format=FORMAT)


def main(keyfile):
    exchange = Bitstamp(keyfile)
    while True:
        logging.info("Start")
        balance = exchange.balance()
        ticker = exchange.ticker()
        usd_amount = balance['usd_balance']
        btc_amount = balance['btc_balance']
        btc_price = (ticker['ask']+ticker['bid'])/2
        logging.info('balance: USD: %.0f, BTC: %.1f' % (usd_amount, btc_amount))
        logging.info('btc price: %.1f' % btc_price)
        btc_in_usd = btc_amount * btc_price

        if usd_amount > btc_in_usd * 1.1:
            btc_buy_amount = (usd_amount - btc_in_usd)/2.0/btc_price
            logging.info('Rebalance: buy BTC and sell USD.  Price = %.2f, amount = %.8f' % (btc_price, btc_buy_amount))
            if btc_buy_amount < 1:
                logging.info("Buy amount < 1, skip")
            else:
                open_orders = exchange.open_orders()
                logging.info("Open orders: %s" % str(open_orders))
                logging.info("Cancel all orders")
                exchange.cancel_all_orders()
                exchange.buy(round(btc_buy_amount, 8), round(btc_price, 2))
        if usd_amount < btc_in_usd/1.1:
            btc_sell_amount = (btc_in_usd - usd_amount)/2.0/btc_price
            logging.info('Rebalance: sell BTC and buy USD.  Price = %.2f, amount = %.8f' % (btc_price, btc_sell_amount))
            if btc_sell_amount < 1:
                logging.info("Sell amount < 1, skip")
            else:
                open_orders = exchange.open_orders()
                logging.info("Open orders: %s" % str(open_orders))
                logging.info("Cancel all orders")
                exchange.cancel_all_orders()
                exchange.sell(round(btc_sell_amount, 8), round(btc_price, 2))

        time.sleep(60)


if __name__ == '__main__':
    main("/home/jftsai/.btc-trading/key/bitstamp")
