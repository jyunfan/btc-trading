#!/usr/bin/env python

MARKET_LTC_BTC = "LTC/BTC"

class market():
    def __init__(self, market):
        self.market = market

    def get_ticker(self):
        depth = self.get_depth()
        res = {'ask': 0, 'bid': 0}
        if len(depth['asks']) > 0 and len(depth["bids"]) > 0:
            res = {'ask': depth['asks'][0],
                   'bid': depth['bids'][0]}
        return res
