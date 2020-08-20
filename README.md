# remesa-bitcoin
 
## Background
 
Sending remittances to Venezuela is not an easy task, first you have government currency controls giving you unfavorable rates. Then you have US sanctions that make banks and other institutions avoid doing business in Venezuela. Fortunately bitcoins and crypto technology offer a solution to these problems, helping immigrants to send money to their loved ones.
 
Unfortunately crypto adoption is not massive, so there is a need to exchange crypto for local currency. This is something that can be easily accomplished using exchanges as https://localbitcoins.com/
 
## Requirements
 
Must install or clone lbcapi3. https://github.com/chidindu-ogbonna/lbcapi3
 
## Use
1) Create a localbitcoins account and then create a HMAC authentication with reading scope https://localbitcoins.com/accounts/api/
2) Write your localbitcoins public and private keys on the `lbclink.py` file, do not upload you private keys or share it with anyone.
3) Modify the user variables (Currency, bank, amount, etc) on the `get_deals.py` file
4) Run the `get_deals.py` file
 
The file will print averages rates and then after a couple of minutes (searching for the right offer) it will print the buy and sell bitcoins ads and open them on your default web browser.
