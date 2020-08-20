"""
@author: Chuox
"""
# TODO: report errors when using conn 

import os #Is recomended to store your private kyes as enviroment variables
import urllib.parse
import re
from lbcapi3 import api
from datetime import datetime, timedelta

hmac_key =  os.environ.get("LBTC_PUBLIC") #your public key here
hmac_secret = os.environ.get("LBTC_PRIVATE") #your private key here

conn = api.hmac(hmac_key, hmac_secret)

def getAveragePrices(fiat):
    fiat = fiat.upper()
    try:
        AveragePrice = conn.call(
                'GET', '/bitcoinaverage/ticker-all-currencies/').json()
    except Exception as e:
        AveragePrice={}
        AveragePrice[fiat] = e
    price = AveragePrice[fiat]
    return price


def getListedAds(operation, fiat, method= None):
    # TODO: return error if method not available
    operation = operation.lower()
    fiat = fiat.lower()
    SalesAds = []
    params = {}
    if method == None:
        endpoint = '/'+operation+'-bitcoins-online/'+fiat+'/.json'
    elif method == 'cash':
        SalesAds = 'cash not allowed'
        return SalesAds
    else:
        method = method.lower()
        endpoint = '/'+operation+'-bitcoins-online/'+fiat+'/'+method+'/.json'
    while True:
        if params == {}:
            SalesAdsTemp = conn.call('GET', endpoint).json()
            SalesAds.extend(SalesAdsTemp['data']['ad_list'])
        else:
            SalesAdsTemp = conn.call('GET', endpoint, params=params).json()
            SalesAds.extend(SalesAdsTemp['data']['ad_list'])
        if 'pagination' in SalesAdsTemp:
            if 'next' in SalesAdsTemp['pagination']:
                parsed = urllib.parse.urlparse(
                    SalesAdsTemp['pagination']['next'])
                params = urllib.parse.parse_qs(
                    parsed.query)
            else:
                return SalesAds
        else:
            return SalesAds


def getQuote(
        operation, fiat, amount, method= None, bank='none',
        listedOffers='none', online='no'):
    Quote = {}
    operation = operation.lower()
    fiat = fiat.lower()
    if listedOffers == 'none':
        listedOffers = getListedAds(operation, fiat, method)
    for x in listedOffers:
        if x['data']['min_amount'] is None:
            x['data']['min_amount'] = '0'
        if x['data']['max_amount'] is None:
            if x['data']['max_amount_available'] is None:
                x['data']['max_amount'] = 'inf'
            else:
                x['data']['max_amount'] = x['data']['max_amount_available']
        if bank == 'none':
            if float(x['data']['min_amount']) < float(amount) < float(x['data']['max_amount']):
                Quote['ad_id'] = x['data']['ad_id']
                Quote['temp_price'] = x['data']['temp_price']
                if online == 'no':
                    return Quote
                elif online == 'online':
                    LastConnection = LastUserConnection(Quote['ad_id'])
                    if LastConnection[1] == 'online':
                        return Quote
                    elif online == 'idle':
                        LastConnection = LastUserConnection(Quote['ad_id'])
                        if LastConnection[1] == 'idle' or LastConnection[1] == 'online':
                            return Quote
                else:
                    fiatLimits = x['data']['limit_to_fiat_amounts'].split(",")
                    for y in fiatLimits:
                        if y == str(amount):
                            Quote['ad_id'] = x['data']['ad_id']
                            Quote['temp_price'] = x['data']['temp_price']
                            if online == 'no':
                                return Quote
                            elif online == 'online':
                                LastConnection = LastUserConnection(Quote['ad_id'])
                                if LastConnection[1] == 'online':
                                    return Quote
                                elif online == 'idle':
                                    LastConnection = LastUserConnection(Quote['ad_id'])
                                    if LastConnection[1] == 'idle' or LastConnection[1] == 'online':
                                        return Quote
        else:
            if re.search(bank, x['data']['bank_name'], re.IGNORECASE):
                if float(x['data']['min_amount']) < float(amount) < float(x['data']['max_amount']):
                    Quote['ad_id'] = x['data']['ad_id']
                    Quote['temp_price'] = x['data']['temp_price']
                    if online == 'no':
                        return Quote
                    elif online == 'online':
                        LastConnection = LastUserConnection(Quote['ad_id'])
                        if LastConnection[1] == 'online':
                            return Quote
                        elif online == 'idle':
                            LastConnection = LastUserConnection(Quote['ad_id'])
                            if LastConnection[1] == 'idle' or LastConnection[1] == 'online':
                                return Quote
    Quote['ad_id'] = 'no offer'
    Quote['temp_price'] = 'no offer'
    return Quote


def LastUserConnection(TradeID):
    endpoint = '/api/ad-get/'+str(TradeID)+'/'
    AdInfo = conn.call('GET', endpoint).json()
    LastTimeOnline = AdInfo['data']['ad_list'][0]['data']['profile']['last_online']
    LastTimeOnlineFormat = datetime.fromisoformat(LastTimeOnline)
    LastTimeOnlinenaive = LastTimeOnlineFormat.replace(tzinfo=None)
    NowUTC = datetime.utcnow()
    TimeDiff = NowUTC-LastTimeOnlinenaive
    if TimeDiff < timedelta(minutes=5):
        status = 'online'
    elif TimeDiff > timedelta(minutes=5) and TimeDiff < timedelta(minutes=60):
        status = 'idle'
    else:
        status = 'offline'
    return [LastTimeOnlineFormat, status]


def oder_by_price(list_to_order, order='ascending'):
    temp_list = []
    temp_ordered_list = []
    ordered_list = []
    index = 0
    for x in list_to_order:
        temp_list = [float(x['data']['temp_price']), index]
        temp_ordered_list.append(temp_list)
        index = index+1
    if order == 'ascending':
        temp_ordered_list.sort()
    else:
        temp_ordered_list.sort(reverse=True)
    for x in temp_ordered_list:
        value = x[1]
        ordered_list.append(list_to_order[value])
    return ordered_list


def ave_rates(ave_sell, ave_buy): 
    rates = {}
    try:
        rates['avg24_rate'] = float(
                ave_buy['avg_24h'])/float(ave_sell['avg_24h'])
    except Exception as e:
        rates['avg24_rate'] = "no average"
        print("{} ".format(e))
    try:
        rates['avg12_rate'] = float(
                ave_buy['avg_12h'])/float(ave_sell['avg_12h'])
    except Exception as e:
        rates['avg12_rate'] = "empty"
        print("{} ".format(e))
    try:
        rates['avg6_rate'] = float(ave_buy['avg_6h'])/float(ave_sell['avg_6h'])
    except Exception as e:
        rates['avg6_rate'] = "empty"
        print("{} ".format(e))
    try:
        rates['avg1_rate'] = float(ave_buy['avg_1h'])/float(ave_sell['avg_1h'])
    except Exception as e:
        rates['avg1_rate'] = "empty"
        print("{} ".format(e))
    return rates
