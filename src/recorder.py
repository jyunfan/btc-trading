""" Record OKcoin market data
"""
import time
import sys
import json
import hashlib
import zlib
import base64
import datetime
import os
import argparse

from okcoin import websocket

global api_key, secret_key
global currency

#business
def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    return  hashlib.md5((sign+'secret_key='+secretKey).encode("utf-8")).hexdigest().upper()
#spot trade
def spotTrade(channel,api_key,secretkey,symbol,tradeType,price='',amount=''):
    params={
      'api_key':api_key,
      'symbol':symbol,
      'type':tradeType
     }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
    sign = buildMySign(params,secretkey)
    finalStr =  "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"',\
                'sign':'"+sign+"','symbol':'"+symbol+"','type':'"+tradeType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    if amount:
        finalStr += ",'amount':'"+amount+"'"
    finalStr+="},'binary':'true'}"
    return finalStr

#spot cancel order
def spotCancelOrder(channel,api_key,secretkey,symbol,orderId):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"','symbol':'"+symbol+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe trades for self
def realtrades(channel,api_key,secretkey):
   params={'api_key':api_key}
   sign=buildMySign(params,secretkey)
   return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"','binary':'true'}}"

# trade for future
def futureTrade(api_key,secretkey,symbol,contractType,price='',amount='',tradeType='',matchPrice='',leverRate=''):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'contract_type':contractType,
      'amount':amount,
      'type':tradeType,
      'match_price':matchPrice,
      'lever_rate':leverRate
    }
    if price:
        params['price'] = price
    sign = buildMySign(params,secretkey)
    finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'"+api_key+"',\
               'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    finalStr += ",'amount':'"+amount+"','type':'"+tradeType+"','match_price':'"+matchPrice+"','lever_rate':'"+leverRate+"'},'binary':'true'}"
    return finalStr

#future trade cancel
def futureCancelOrder(api_key,secretkey,symbol,orderId,contractType):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId,
      'contract_type':contractType
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_futuresusd_cancel_order','parameters':{'api_key':'"+api_key+"',\
            'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe future trades for self
def futureRealTrades(api_key,secretkey):
    params = {'api_key':api_key}
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_usd_future_realtrades','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'},'binary':'true'}"

def on_open(self):
    '''
    Args:
    '''
    global currency
    if currency == 'cny':
        pass
    else:
        channels = [
                'ok_btcusd_depth',
                'ok_btcusd_trades_v1',
                'ok_ltcusd_depth',
                'ok_ltcusd_trades_v1',

                'ok_btcusd_future_depth_this_week',
                'ok_btcusd_future_depth_next_week',
                'ok_btcusd_future_depth_quarter',
                'ok_btcusd_future_trade_v1_this_week',
                'ok_btcusd_future_trade_v1_next_week',
                'ok_btcusd_future_trade_v1_quarter',
            ]
    for channel in channels:
        ret = self.send("{'event':'addChannel','channel':'%s','binary':'true'}" % channel)


def on_message(self,evt):
    data = inflate(evt) #data decompress
    recorder.write(data)


def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_error(self,evt):
    print("Error:", evt)


def on_close(self,evt):
    print('DISCONNECT')


class Recorder:
    def __init__(self, logdir):
        self.logdir = logdir
        self.fh = None
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.update_filehandler()


    def update_filehandler(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if self.fh == None or today > self.today:
            self.today = today
            if self.fh is not None:
                self.fh.close()
            self.fh = open(os.path.join(self.logdir, today + '.log'), 'a')


    def write(self, msg):
        fh = self.fh
        self.update_filehandler()
        print('.', end='')
        fh.write(msg.decode() + '\n')
        fh.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--currency', help='cny|usd')
    args = parser.parse_args()


    if args.currency == 'cny':
        url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
    elif args.currency == 'usd':
        url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
    else:
        args.help()
        sys.exit(1)

    global currency
    currency = args.currency
    global recorder

    logdir = "okcoin_%s" % args.currency
    try:
        os.mkdir(logdir)
    except:
        pass

    recorder = Recorder(logdir)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    print('Start websocket')
    ws.run_forever()
