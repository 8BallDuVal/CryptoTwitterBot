import requests 
import tweepy

r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=11')

prices = []
symbols = []
change = []
market_cap = []

for coin in r.json():
    ticker = '#'+coin.get("symbol", "Cryptocurrency Name Note Provided")
    symbols.append(ticker)
    
    price = float(coin.get("price_usd", "US$ Price not provided"))
    test = round(price, 3)
    prices.append(test)
    
    percent = '('+ coin.get("percent_change_1h", "Percent Change not provided")+'%)'
    change.append(percent)
    

#print(symbols)
#print(prices)
#print(change)
pricedata = []
for i in range(len(symbols)):
    pricedata.append(str(symbols[i] +': '+ str(prices[i]) +' '+ change[i]+'\n'))

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


# This information is found after creating an account at https://developer.twitter.com/
# See more information at the following link: http://docs.tweepy.org/en/v3.5.0/api.html#status-methods 
# This tutorial may also be helpful: https://scotch.io/tutorials/build-a-tweet-bot-with-python
# consumer_key = ''
# consumer_secret = ''
# access_token = ''
# access_token_secret = ''
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
#   
# api.update_status(final_pricedata)

print(final_pricedata)



