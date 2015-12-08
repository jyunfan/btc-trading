#coding=utf-8

""" Rebalance cash and BTC
"""

import argparse
import time
import logging
from datetime import datetime
import subprocess

from Bitstamp import Bitstamp
from Huobi import Huobi

FORMAT = '%(asctime)-15s %(module)s %(message)s'
logging.basicConfig(level=logging.INFO, filename='rebalance.log', format=FORMAT)
#logging.basicConfig(level=logging.INFO, format=FORMAT)


def main(exchange_name, keyfile, min_trade_btc=0.01, min_price_change=1.01, fiat='usd', sleep_second=60):
    min_trade_btc = 0.001
    min_price_change = 1.001

    # When account is balance, we create buy and sell limit order at expect price change
    expect_price_change = 1.002

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
        logging.info("Loop")

        logging.info("Cancel existing orders")
        exchange.cancel_all_orders(coin)

        balance = exchange.balance()
        fiat_amount = balance[fiat + '_balance']
        btc_amount = balance['btc_balance']
        logging.info('balance: FIAT: %.2f, BTC: %.2f' % (fiat_amount, btc_amount))

        ticker = exchange.ticker()
        btc_price = (ticker['ask']+ticker['bid'])/2

        logging.info('btc price: %.2f' % btc_price)
        btc_in_fiat = btc_amount * btc_price

        logging.info("FIAT/COIN=%.4f" % (fiat_amount / btc_in_fiat))
        if fiat_amount > btc_in_fiat * min_price_change:
            btc_buy_amount = (fiat_amount - btc_in_fiat)/2.0/btc_price
            logging.info('Rebalance: buy BTC and sell FIAT.  Price = %.2f, amount = %.8f' % (btc_price, btc_buy_amount))
            if btc_buy_amount < min_trade_btc:
                logging.info("Buy amount < min_trade_btc, skip")
            else:
                exchange.buy(round(btc_buy_amount, amount_digits), round(btc_price, price_digits))
        elif fiat_amount < btc_in_fiat / min_price_change:
            btc_sell_amount = (btc_in_fiat - fiat_amount)/2.0/btc_price
            logging.info('Rebalance: sell BTC and buy FIAT.  Price = %.2f, amount = %.8f' % (btc_price, btc_sell_amount))
            if btc_sell_amount < min_trade_btc:
                logging.info("Sell amount < min_trade_btc, skip")
            else:
                exchange.sell(round(btc_sell_amount, amount_digits), round(btc_price, price_digits))
        else:
            pass
            # logging.info('Almost balance.  Put expected buy and sell limit order')
            # # Expect price of coin fail
            # expect_btc_price = btc_price / expect_price_change
            # expect_btc_in_fiat = btc_in_fiat / expect_price_change
            # btc_buy_amount = (fiat_amount - expect_btc_in_fiat)/2.0/expect_btc_price
            # logging.info('Expected Rebalance: buy BTC and sell FIAT.  Price = %.2f, amount = %.8f' % (expect_btc_price, btc_buy_amount))
            # if btc_buy_amount > min_trade_btc:
            #     exchange.buy(round(btc_buy_amount, amount_digits), round(expect_btc_price, price_digits))
            #
            # # Expect price of coin raise
            # expect_btc_price = btc_price * expect_price_change
            # expect_btc_in_fiat = btc_in_fiat * expect_price_change
            # btc_sell_amount = (expect_btc_in_fiat - fiat_amount)/2.0/expect_btc_price
            # logging.info('Expected Rebalance: sell BTC and buy FIAT.  Price = %.2f, amount = %.8f' % (expect_btc_price, btc_sell_amount))
            # if btc_sell_amount > min_trade_btc:
            #     exchange.sell(round(btc_sell_amount, amount_digits), round(expect_btc_price, price_digits))

        time.sleep(sleep_second)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyfile', required=True)
    parser.add_argument('-f', '--fiat', required=True)
    parser.add_argument('--exchange', required=True)
    parser.add_argument('--min_trade_btc', required=True, type=float)
    parser.add_argument('--min_price_change', required=True, type=float)
    parser.add_argument('--sleep', required=True, type=int)
    args = parser.parse_args()

    main(args.exchange, args.keyfile, min_trade_btc=args.min_trade_btc, min_price_change=args.min_price_change, fiat=args.fiat, sleep_second=args.sleep)
