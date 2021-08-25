# import necessary libraries 
from configparser import ConfigParser
import alpaca_trade_api as tradeapi 
import pandas as pd

# Test Connection
# Parse the config file
config = ConfigParser()
config.read('config.ini')

# Access the authorization passwords
API_KEY = config['keys']['API_KEY']
API_SECRET = config['keys']['API_SECRET']
BASE_URL = config['keys']['ENDPOINT']

api_key = API_KEY
api_secret = API_SECRET
base_url = BASE_URL

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Get all the stocks 
active_assets = api.list_assets(status='active')
stock_list = []
keys = range(len(stock_list))
for asset in active_assets:
    stock_list.append(asset.symbol)

# Convert into a dictionary
stock_tickers = {}
keys = range(len(stock_list))
values = stock_list
for i in keys:
        stock_tickers[i] = stock_list[i]
print(stock_tickers)

# load into a pandas dataframe
pd.DataFrame(stock_ticker)