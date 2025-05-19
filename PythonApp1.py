import yfinance as yf
from datetime import datetime

# Define tickers
tickers = ['MSFT', 'AAPL', 'MSTR']
qtys = [100, 400, 97]

# Get today's date and first trading day of the year
today = datetime.today().strftime('%Y-%m-%d')
start_of_year = f'{datetime.today().year}-01-01'

print('Ticker Close YTD % Change')
print("-" * 35)

for ticker in tickers:
   try:
       data = yf.download(ticker, 
             start=start_of_year, 
             end=today,progress=False)
       if not data.empty:
            close = data['Close']
            ytd_open = data['Close'].iloc[0]
            latest_close = data['Close'].iloc[-1]
            ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
            print(f"{ticker:<6} {latest_close.item():>10.2f} {ytd_pct_change.item():>14.2f}%")
       else:
            print(f"{ticker:<6} {'N/A':>10} {'N/A':>15}")
   except Exception as e:
           print(f"{ticker:<6} {'ERROR':>10} {'N/A':>15}  ({e})")
