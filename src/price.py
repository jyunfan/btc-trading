#!/usr/bin/python

import json
import logging
import pandas as pd
import requests

# Produce formater first
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup Handler
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

# Setup Logger
logger = logging.getLogger( __name__ )
logger.addHandler(console)
logger.setLevel(logging.DEBUG)

# r is number of days, i is the interval
querystring = 'http://bitcoincharts.com/charts/chart.json?m=bitstampUSD&r=3&i=1-min'

""" Get current simple average prices given window sizes.
    [a,b] = get_current_price([120, 1440])

    return 0 if there is any exception or number is too low or too high
    window -- window size in minutes between 1 and 1440
"""
def get_current_price(windows):
    price_min = 100
    price_max = 1000

    if type(windows) != list and type(windows) != tuple:
        windows = [windows]

    try:
        req = requests.get(querystring)
        if req.status_code != 200:
            return 0

        prices = json.loads(req.content)
        if len(prices) < max(windows):
            logger.debug("Number of price is less then window size %d" % window)
            return 0

        # Get latest prices
        df = pd.DataFrame(prices)

        price_cur = []
        for w in windows:
            # We use some weighting here.
            # For example, volume weighting: weighted current price = total currency / total BTC
            price_in_window = df[7][-w:]
            # handle zero values
            p = price_in_window[price_in_window > 0.01].mean()
            if p < price_min or p > price_max:
                logger.debug("Number of price %d is out of range" % p)
                return 0
            price_cur.append(p)

        return price_cur

    except:
        logger.warn("get price error")
        return 0
