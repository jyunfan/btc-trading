'''
Extract quotes and ticks from exchange logs.
Support okcoin

Output Format:
Quote:
<timestamp in nanosecond> bid_1 ask_1 bid_2 ask_2 ...

Input Example:
[{ "channel":"ok_btccny_depth","data":{"bids":[[2885.6,0.026],[2885.55,0.028]],"asks":[[2886.67,0.04],[2886.62,0.045]],"timestamp":"1450013738538"}}]

okcoin future:
[{"channel":"ok_btcusd_future_depth_this_week","data":{"bids":[[445.55,2],[445.53,208],[445.42,1],[445.31,20],[444.99,1],[444.98,218],[444.94,125],[444.79,16],[444.69,8],[444.45,2],[444.25,30],[444.22,6],[444.2,5],[444.06,6],[444.05,9],[443.82,2],[443.8,30],[443.73,27],[443.72,2],[443.65,10]],"asks":[[447.97,67],[447.96,40],[447.64,50],[447.5,126],[447.3,47],[447.15,27],[447.14,35],[447.1,7],[447,55],[446.92,39],[446.84,12],[446.7,2],[446.51,5],[446.4,12],[446.34,6],[446.28,1],[446.11,6],[445.82,20],[445.78,9],[445.75,16]],"timestamp":"1450002898572","unit_amount":100}}]
[{"channel":"ok_btcusd_future_depth_next_week","data":{"bids":[[446.54,11],[446.47,11],[445.82,4],[445.55,50],[445.5,5],[445.4,1],[445.27,10],[445.14,10],[445.08,10],[445.04,8],[445.02,4],[445.01,10],[445,1],[444.98,89],[444.95,1636],[444.89,20],[444.6,1],[444.5,30],[444.39,50],[444.23,4]],"asks":[[450.02,17],[449.84,1990],[449.61,224],[449.47,50],[449.46,40],[449.3,2052],[449.29,40],[449.16,13],[449.15,13],[449.13,4],[448.96,27],[448.83,10],[448.72,10],[448.51,10],[448.48,10],[448.28,10],[448.25,4],[448.23,50],[447.85,2],[447.32,39]],"timestamp":"1450002898573","unit_amount":100}}]
'''

import argparse
import json
import os
import gzip

import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def parse_okcoin(symbol, infile, output_folder, maxlevel=10, out_format='gzip'):
    if symbol == 'cny':
        quote_channels = [ 'ok_btccny_depth' ]
        contract = [['OKCOIN_BTCCNY', 'BTCCNY']]
    else:
        quote_channels = [
            'ok_btcusd_depth',
            'ok_btcusd_future_depth_this_week',
            'ok_btcusd_future_depth_next_week',
            'ok_btcusd_future_depth_quarter']
        contract = [
            ['OKCOIN_BTCUSD', 'BTCUSD'],
            ['OKCOIN_BTCUSD', 'BTCUSDW'],
            ['OKCOIN_BTCUSD', 'BTCUSDNW'],
            ['OKCOIN_BTCUSD', 'BTCUSDQ'],
            ]
    fmap = dict(zip(quote_channels, range(0,len(quote_channels))))
    fout = [0]*len(fmap)
    for i in range(0,len(fout)):
        contract_dir = os.path.join(output_folder, contract[i][0])
        mkdir_p(contract_dir)
        contract_file = os.path.join(contract_dir, contract[i][1] + '.csv')
        if out_format == 'gzip':
            fout[i] = gzip.open(contract_file + '.gz', 'wt')
        else:
            fout[i] = open(contract_file, 'w')
    fid = gzip.open(infile, 'rt')
    for line in fid:
        info = json.loads(line)[0]
        if info['channel'] in quote_channels:
            data = info['data']
            quote = [data['timestamp']]
            bids = data['bids']
            asks = data['asks']
            asks.reverse()
            level = min(maxlevel, len(bids), len(asks))
            bids = bids[0:level]
            asks = asks[0:level]
            for (bid,ask) in zip(bids,asks):
                quote.append('%s@%s\t%s@%s' % (bid[0], bid[1], ask[0], ask[1]))
            fo = fout[fmap[info['channel']]]
            quotestr = '\t'.join(quote)
            fo.write(quotestr + '\n')

    for f in fout:
        f.close()

def main(symbol, infile, outputprefix):
    parse_okcoin(symbol, infile, outputprefix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process exchange log')
    parser.add_argument('--input', required=True)
    parser.add_argument('--outputdir', required=True)
    parser.add_argument('--symbol', required=True)
    args = parser.parse_args()
    main(args.symbol, args.input, args.outputdir)
