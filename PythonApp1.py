import yfinance as yf
import pandas as pd 
from datetime import datetime

# Define tickers
tickers = ['MSFT', 'AAPL', 'MSTR']
qtys = [100, 400, 97]

# Get today's date and first trading day of the year
today = datetime.today().strftime('%Y-%m-%d')
start_of_year = f'{datetime.today().year}-01-01'

print('Ticker  Close     YTD % Change')
print("-" * 35)

results = []

for ticker in tickers:
    try:
        data = yf.download(
            ticker,
            start=start_of_year,
            end=today,
            progress=False,
            auto_adjust=False
        )
        if not data.empty and 'Close' in data:
            close = data['Close']
            # If close is a DataFrame, select the column for the ticker
            if isinstance(close, pd.DataFrame):
                if ticker in close.columns:
                    close = close[ticker]
                else:
                    results.append((ticker, None, None))
                    continue
            if len(close) > 1:
                ytd_open = float(close.iloc[0])
                latest_close = float(close.iloc[-1])
                ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
                results.append((ticker, latest_close, ytd_pct_change))
            else:
                results.append((ticker, None, None))
        else:
            results.append((ticker, None, None))
    except Exception:
        results.append((ticker, 'ERROR', None))

# Sort by YTD % Change descending, handling None values
results_sorted = sorted(
    results,
    key=lambda x: (x[2] is not None, x[2] if x[2] is not None else float('-inf')),
    reverse=True
)

for ticker, latest_close, ytd_pct_change in results_sorted:
    if latest_close is None:
        print(f"{ticker:<6} {'N/A':>10} {'N/A':>15}")
    elif latest_close == 'ERROR':
        print(f"{ticker:<6} {'ERROR':>10} {'N/A':>15}")
    else:
        print(f"{ticker:<6} {latest_close:>10.2f} {ytd_pct_change:>14.2f}%")




