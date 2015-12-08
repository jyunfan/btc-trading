#coding=utf-8

import time
import requests
import hashlib

try:
    # python 2
    from urllib import urlencode
except ImportError:
    # python 3
    from urllib.parse import urlencode

ACCESS_KEY=""
SECRET_KEY=""
TRADE_PASS=""

HUOBI_SERVICE_API="https://api.huobi.com/apiv3"

BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
ACCOUNT_INFO = "get_account_info"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
SELL = "sell"
SELL_MARKET = "sell_market"

TIMEOUT = 10

def signature(params):
    params = sorted(zip(params.keys(), params.values()), key=lambda d:d[0], reverse=False)
    message = urlencode(params)
    m = hashlib.md5()
    m.update(message.encode('utf-8'))
    m.digest()
    sig=m.hexdigest()
    return sig

'''
÷lAH±¡
'''
def getAccountInfo():
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"method":'get_account_info'}
    sign=signature(params)
    params['sign']=sign

    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
¤U˱µ¤f
@param coinType
@param price
@param amount
@param tradePassword
@param tradeid
@param method
'''
def buy(coinType,price,amount,tradePassword,tradeid,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"price":price,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
´£¥楫ɲ˱µ¤f
@param coinType
@param amount
@param tradePassword
@param tradeid
'''

def buyMarket(coinType,amount,tradePassword,tradeid,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None


'''
ºM¦zË@param coinType
@param id
'''

def cancelOrder(coinType,id,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"id":id,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
¬dRª¤H³̷s10W¦¨¥æË@param coinType
'''
def getNewDealOrders(coinType,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
®Úutrade_id¬dRoder_id
@param coinType
@param tradeid
'''
def getOrderIdByTradeId(coinType,tradeid,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"trade_id":tradeid}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
÷Ҧ³¥¿¦bn¦檺©e¦«
@param coinType
'''
def getOrders(coinType,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
÷zˆH±¡
@param coinType
@param id
'''
def getOrderInfo(coinType,id,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"id":id}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
­­ɲo¥X
@param coinType
@param price
@param amount
@param tradePassword
@param tradeid
'''
def sell(coinType,price,amount,tradePassword,tradeid,method):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"price":price,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload, timeout=TIMEOUT)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None

'''
¥«ɲo¥X
@param coinType
@param amount
@param tradePassword
@param tradeid
'''
def sellMarket(coinType,amount,tradePassword,tradeid,method, timeout=TIMEOUT):
    timestamp = int(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    del params['secret_key']

    payload = urlencode(params)
    r = requests.post(HUOBI_SERVICE_API, params=payload)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None


def ticker(coin):
    """
    {'bid':<float>,'ask':<float>}
    amount?
    https://github.com/huobiapi/API_Docs/wiki/REST-Order-Book-and-TAS
    """
    if coin == 'btc':
        url = 'http://api.huobi.com/staticmarket/detail_btc_json.js'
    elif coin == 'ltc':
        url = 'http://api.huobi.com/staticmarket/detail_ltc_json.js'
    r = requests.get(url)
    ret = r.json()
    ret['bid'] = ret['top_buy'][0]['price']
    ret['ask'] = ret['top_sell'][0]['price']
    return ret
