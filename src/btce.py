#!/usr/bin/env python

class BtceMarker(Market):
    def __init__(self, market):
        super(BtceMarket, self).__init(market)

    def update_depth(self):
        url = 'https://btc-e.com/api/2/btc_usd/depth'
