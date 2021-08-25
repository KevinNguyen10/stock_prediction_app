# import necessary libraries
import streamlit as st
from datetime import date
import yfinance as yf 
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go 
import plotly.graph_objects as go
from configparser import ConfigParser
import alpaca_trade_api as tradeapi 

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

# Select a start and todays date
START = "2015-01-01"
TODAY = date.today().strftime('%Y-%m-%d')

# Streamlit title
st.title("Stock Prediction App")

# Selected Stocks
# Get all the stocks 
active_assets = api.list_assets(status='active')
stock_list = []
keys = range(len(stock_list))
for asset in active_assets:
    stock_list.append(asset.symbol)
stocks = (tuple(stock_list))

# Dropdown menu
selected_stocks = st.selectbox('Select dataset for prediction', stocks)

# years slider
n_years = st.slider('years of prediction:', 1, 4)
period = n_years * 365

# cache will save the data so it will not have to load it again
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Load data...')
data = load_data(selected_stocks)
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))
    fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(data.tail())

st.write('forecast data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)