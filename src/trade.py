#!/usr/bin/env python
# Command line interface for exchange.
# You can buy, sell, get balance, etc.

import argparse

import bitstamp

def main(args):
    if args['exchange'] == 'bitstamp':
        exchange = Bitstamp()

    if args['action'] == 'get-balance':
        print exchange.get_balance()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='get-balance')
    parser.add_argument('-e', '--exchange', default='bitstamp')
    args = parser.parse_args()
    main()
    pass
