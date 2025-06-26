import yfinance as yf
from datetime import datetime
import pandas as pd

# Test with AAPL to see what data we get
ticker = 'AAPL'
today = datetime.today().strftime('%Y-%m-%d')
start_of_year = f'{datetime.today().year}-01-01'

print(f'Fetching data for {ticker} from {start_of_year} to {today}')

# Test yfinance download
data = yf.download(ticker, start=start_of_year, end=today, progress=False, auto_adjust=False)
print(f'Data shape: {data.shape}')
print(f'Last few rows:')
print(data.tail())

# Test with latest date
if not data.empty:
    latest_close = data['Close'].iloc[-1]
    print(f'Latest close price: {latest_close}')
    print(f'Latest date: {data.index[-1]}')
    
# Also test real-time data
print('\n--- Testing real-time data ---')
ticker_obj = yf.Ticker(ticker)
info = ticker_obj.info
print(f'Current price from info: {info.get("currentPrice", "N/A")}')
print(f'Regular market price: {info.get("regularMarketPrice", "N/A")}')
print(f'Previous close: {info.get("previousClose", "N/A")}')

# Test fast_info
fast_info = ticker_obj.fast_info
print(f'Last price from fast_info: {fast_info.get("last_price", "N/A")}')
print(f'Previous close from fast_info: {fast_info.get("previous_close", "N/A")}')

# Test current market hours
print('\n--- Testing market status ---')
try:
    from yfinance.domain.market import Market
    market = Market('us_market')
    print(f'Market status: {market.status}')
except Exception as e:
    print(f'Could not get market status: {e}')

# Test with period=1d to get most recent data
print('\n--- Testing with period=1d ---')
recent_data = ticker_obj.history(period="1d", interval="1m")
if not recent_data.empty:
    print(f'Most recent minute data: {recent_data.tail(1)}')
    print(f'Last trade time: {recent_data.index[-1]}')

# Test history with live data
print('\n--- Testing live data inclusion ---')
live_data = ticker_obj.history(period="5d", interval="1d", prepost=True)
if not live_data.empty:
    print(f'Live data (last 3 rows):')
    print(live_data.tail(3))
