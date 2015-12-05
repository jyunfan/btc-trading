""" Rebalance cash and BTC
"""

import argparse
import time
import logging
from datetime import datetime
from Bitstamp import Bitstamp
from Huobi import Huobi

FORMAT = '%(asctime)-15s %(module)s %(message)s'
#logging.basicConfig(level=logging.INFO, filename='rebalance.log', format=FORMAT)
logging.basicConfig(level=logging.INFO, format=FORMAT)


def main(exchange_name, keyfile, fiat='usd', sleep_second=60):
    min_trade_btc = 0.04
    coin = 'btc'
    amount_digits = 4
    price_digits = 2

    if exchange_name == 'huobi':
        exchange = Huobi(keyfile)
    elif exchange_name == 'bitstamp':
        exchange = Bitstamp(keyfile)
    else:
        print('unknown exchange name')
        return

    while True:
        logging.info("Start")
        balance = exchange.balance()

        fiat_amount = balance[fiat + '_balance']
        btc_amount = balance['btc_balance']
        logging.info('balance: FIAT: %.2f, BTC: %.2f' % (fiat_amount, btc_amount))

        ticker = exchange.ticker()
        btc_price = (ticker['ask']+ticker['bid'])/2

        logging.info('btc price: %.2f' % btc_price)
        btc_in_fiat = btc_amount * btc_price

        if fiat_amount > btc_in_fiat * 1.1:
            btc_buy_amount = (fiat_amount - btc_in_fiat)/2.0/btc_price
            logging.info('Rebalance: buy BTC and sell FIAT.  Price = %.2f, amount = %.8f' % (btc_price, btc_buy_amount))
            if btc_buy_amount < min_trade_btc:
                logging.info("Buy amount < min_trade_btc, skip")
            else:
                open_orders = exchange.open_orders(coin)
                logging.info("Open orders: %s" % str(open_orders))
                logging.info("Cancel all orders")
                exchange.cancel_all_orders(coin)
                exchange.buy(round(btc_buy_amount, 8), round(btc_price, 2))
        if fiat_amount < btc_in_fiat/1.1:
            btc_sell_amount = (btc_in_fiat - fiat_amount)/2.0/btc_price
            logging.info('Rebalance: sell BTC and buy FIAT.  Price = %.2f, amount = %.8f' % (btc_price, btc_sell_amount))
            if btc_sell_amount < min_trade_btc:
                logging.info("Sell amount < min_trade_btc, skip")
            else:
                open_orders = exchange.open_orders(coin)
                logging.info("Open orders: %s" % str(open_orders))
                logging.info("Cancel all orders")
                exchange.cancel_all_orders(coin)
                exchange.sell(round(btc_sell_amount, amount_digits), round(btc_price, price_digits))

        time.sleep(sleep_second)


if __name__ == '__main__':
    #main("/home/jftsai/.btc-trading/key/bitstamp")
    sleep = 20
    main('huobi', "/home/jftsai/.btc-trading/key/huobi", 'cny', sleep)
