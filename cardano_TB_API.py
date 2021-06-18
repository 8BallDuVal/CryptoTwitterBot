import tweepy
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':'ADA',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '',
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
    for key, value in cryptodata.items():                               # full dictionary
        if key == 'data':
            for k,v in value.items():                                   # 'Data' dictionary within full dictionary
                for key_1,value_1 in v.items():
                    if key_1 == 'quote':
                        for key_2, value_2 in value_1.items():          # "Quote" dictionary, within the 'Data' dictionary, within the full dictionary
                            for key_3, value_3 in value_2.items():      # Drilling into the 'USD' dictionary, within the "Quote" dictionary, within the 'Data' dictionary, within the full dictionary
                                if key_3 == 'price':
                                    price_rounded = str(round(float(value_3), 6))                        #rounding the prices to 3 decimals to save characters on twitter
                                elif key_3 == 'percent_change_24h':
                                    percent_change_rounded = str(round(float(value_3), 3)) + '%'         #rounding values to 3 decimals as done above

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  

pricedata = str('The current price of #Cardano is: $'+ str(price_rounded) +' ('+ percent_change_rounded+' in the past 24 hours) \n\n$ADA')


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
   
api.update_status(pricedata)

#print(pricedata)