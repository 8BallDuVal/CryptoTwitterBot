import tweepy
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'11',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '',                                                  # info from coinmarketcap.com/api/
}

session = Session()
session.headers.update(headers)
symbols = []
price = []
percent_change = []
cc_data = []
try:
    response = session.get(url, params=parameters)
    cryptodata = json.loads(response.text)
    for key, value in cryptodata.items():
        if key == 'data':
            for item in value:
                for key_1,value_1 in item.items():
                    if key_1 == 'quote':
                        price_rounded = round(float(value_1['USD']['price']), 3)                        # rounding the prices to 3 decimals to save characters on twitter
                        price.append(str(price_rounded))                                                # storing the rounded prices into an array
                        percent_change_rounded = round(float(value_1['USD']['percent_change_24h']), 2)  # rounding values to 3 decimals as done above
                        percent_change.append('('+str(percent_change_rounded) + '%)')                   # storing Percent change in 24 hours into an array
                    if key_1 == 'symbol':
                        symbol = '$' + value_1
                        symbols.append(symbol)                                                          # Cryptocurrency ticker symbol/acronym
               

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  
pricedata = []
for i in range(len(symbols)):
    pricedata.append(str(symbols[i] +': '+ str(price[i]) +' '+ percent_change[i]+'\n'))

final_pricedata = (pricedata[0] + 
                  pricedata[1] +
                  pricedata[2] +
                  pricedata[3] +
                  pricedata[4] +
                  pricedata[5] +
                  pricedata[6] +
                  pricedata[7] +
                  pricedata[8] +
                  pricedata[9] +
                  pricedata[10])

consumer_key = ''                                                           # info from developer.twitter.com
consumer_secret = ''                                                        # info from developer.twitter.com
access_token = ''                                                           # info from developer.twitter.com
access_token_secret = ''                                                    # info from developer.twitter.com
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
   
api.update_status(final_pricedata)
