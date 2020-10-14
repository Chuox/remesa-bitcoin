"""
This file is te file that needs to be executed
in order to get the open trades to do the remmitances
@author: Chuox
"""

import webbrowser
import lbclink

#User Variables
fiatSell = 'COP' #Fiat to sell, currency ISO code to be gaved in exchange of Bitcoins, Example: Colombian pesos
fiatBuy = 'VES' #Fiat to buy, currency ISO code to be recieved in exchange of Bitcoins, Example: Venezuelan Bolivars
amount_sell = 50000 #Amount of fiat to be gaved in exchange of Bitcoins
amount_buy = 50000*84.47 #Amount to be recieved in exchange of Bitcoins
methodSell = None #Example: 'transferencias-con-un-banco-especifico'
methodBuy = None #Example: 'transferencias-con-un-banco-especifico'
bankSell = 'Bancolombia' #Bank where you want to do the fiat payment (Zelle, bofa, etc)
bankBuy = 'Banesco' #Bank where you want to recive the fiat payment (Provincial, Banesco, etc)

# TODO: Use F-Strings to print
ave_sell_prices = lbclink.getAveragePrices(fiatSell)
ave_buy_prices = lbclink.getAveragePrices(fiatBuy)
rates = lbclink.ave_rates(ave_sell_prices, ave_buy_prices)
print(
    'average rate 24h {} {}/{}'.format(
        rates['avg24_rate'],fiatBuy,fiatSell))
print(
    'average rate 12h {} {}/{}'.format(
        rates['avg12_rate'],fiatBuy,fiatSell))
print(
    'average rate 6h {} {}/{}'.format(
        rates['avg6_rate'],fiatBuy,fiatSell))
print(
    'average rate 1h {} {}/{}'.format(
        rates['avg1_rate'],fiatBuy,fiatSell))


listedOffersSell = lbclink.getListedAds(
        'buy', fiatSell, method=methodSell)
listedOffersBuy = lbclink.getListedAds(
        'sell', fiatBuy, method=methodBuy)
listedOffersSell_P = lbclink.oder_by_price(listedOffersSell)
listedOffersBuy_P = lbclink.oder_by_price(listedOffersBuy, order='des')

BestSellOffer = lbclink.getQuote(
        'buy', fiatSell, amount_sell, method=methodSell,
        bank=bankSell, listedOffers=listedOffersSell)
BestBuyOffer = lbclink.getQuote(
        'sell', fiatBuy, amount_buy, method=methodBuy,
        bank=bankBuy, listedOffers=listedOffersBuy)

if BestBuyOffer['temp_price'] == 'no offer':
    print('no offer')
else:
    url1 = 'https://localbitcoins.com/ad/'+str(BestBuyOffer['ad_id'])
    url2 = 'https://localbitcoins.com/ad/'+str(BestSellOffer['ad_id'])
    print(url1)
    print(url2)
    print(fiatBuy + "/BTC " + str(BestBuyOffer['temp_price']))
    print(fiatSell + "/BTC " + str(BestSellOffer['temp_price']))
    current_rate = float(BestBuyOffer['temp_price'])/float(
            BestSellOffer['temp_price'])
    print(current_rate)
    webbrowser.open(url1)
    webbrowser.open(url2)