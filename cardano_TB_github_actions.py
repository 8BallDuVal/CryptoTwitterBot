import tweepy
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os

consumer_key_ghs = os.environ.get("CONSUMER_KEY")
consumer_secret_ghs = os.environ.get("CONSUMER_SECRET")
access_token_ghs = os.environ.get("ACCESS_TOKEN")
access_token_secret_ghs = os.environ.get("ACCESS_TOKEN_SECRET")
cmc_key_ghs = os.environ.get("CMC_KEY")

def send_request(fiat_currency):
    info = []
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'symbol':'ADA',
    'convert': fiat_currency
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': cmc_key_ghs,
    }

    session = Session()
    session.headers.update(headers)
    
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
                                        info.append(price_rounded)
                                    elif key_3 == 'percent_change_24h':
                                        percent_change_rounded = str(round(float(value_3), 3)) + '%'         #rounding values to 3 decimals as done above
                                        info.append(percent_change_rounded)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    return info

# Requesting USD info
usd_data = send_request('USD')
# Requesting GBP info
gbp_data = send_request('GBP')
# Requesting EUR info
eur_data = send_request('EUR')

usd_text = 'The current price of #Cardano is: \n$'+ str(usd_data[0]) +' ('+ usd_data[1]+' in the past 24 hours)\n'
gbp_text = '£'+ str(gbp_data[0]) +' ('+ gbp_data[1]+' in the past 24 hours)\n'
eur_text = '€'+ str(eur_data[0]) +' ('+ eur_data[1]+' in the past 24 hours)\n'

pricedata = usd_text + gbp_text+ eur_text + '\n$ADA'


consumer_key = consumer_key_ghs
consumer_secret = consumer_secret_ghs
access_token = access_token_ghs
access_token_secret = access_token_secret_ghs
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
   
api.update_status(pricedata)

#print(pricedata)
