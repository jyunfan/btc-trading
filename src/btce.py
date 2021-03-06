#!/usr/bin/env python

import argparse
import requests
import logging

import market
from market import Market

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class MarketBtce(Market):
    def __init__(self, market_id):
        super(MarketBtce, self).__init__(market_id)

    def update_depth(self):
        if self.market_id == 'LTC/BTC':
            market_str = 'ltc_btc'
        elif self.market_id == 'BTC/USD':
            market_str = 'btc_usd'
        else:
            raise Exception('Unknown market')

        url = 'https://btc-e.com/api/2/%s/depth' % market_str
        self.depth = {}
        try:
            r = requests.get(url)
            self.depth = self.format_depth(r.json())
        except ValueErorr as e:
            logger.warn("Cannot get depth")

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({'price': float(i[0]), 'amount': float(i[1])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth['bids'], True)
        asks = self.sort_and_format(depth['asks'], False)
        return {'asks': asks, 'bids': bids}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--marketid', help='Market ID: e.g. LTC/BTC', default='LTC/BTC')
    args = parser.parse_args()

    market = MarketBtce(args.marketid)
    print(market.get_ticker())
