#!/usr/bin/env python

import argparse
import requests
import logging

import market
from market import Market

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class MarketCryptsy(Market):
    def __init__(self, market_id):
        super(MarketCryptsy, self).__init__(market_id)

    def update_depth(self):
        if self.market_id == 'LTC/BTC':
            market_str = '3'
        else:
            raise Exception('Unknown market')

        url = 'http://pubapi.cryptsy.com/api.php?method=singleorderdata&marketid=%s' % market_str
        self.depth = {}
        try:
            r = requests.get(url).json()
            depth = r['return'].values()[0]
        except ValueError as e:
            logger.warn("Cannot get depth")
        self.depth = self.format_depth(depth)

    def sort_and_format(self, l, reverse=False):
        r = []
        for i in l:
            r.append({'price': float(i['price']), 'amount': float(i['quantity'])})

        r.sort(key=lambda x: x['price'], reverse=reverse)
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['buyorders'], True)
        asks = self.sort_and_format(depth['sellorders'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--marketid', help='Market ID: e.g. LTC/BTC', default='LTC/BTC')
    args = parser.parse_args()

    market = MarketCryptsy(args.marketid)
    print(market.get_ticker())
