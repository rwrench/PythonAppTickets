import yfinance as yf
import pandas as pd 
from datetime import datetime

tickers = ['MSFT', 'AAPL', 'MSTR']
qtys = [100, 400, 97]

today = datetime.today().strftime('%Y-%m-%d')
start_of_year = f'{datetime.today().year}-01-01'

# Define column widths
ticker_w = 8
close_w = 12
ytd_w = 16

# Print header with matching widths
print(f"{'Ticker':<{ticker_w}}{'Close':>{close_w}}{'YTD % Change':>{ytd_w}}")
print("-" * (ticker_w + close_w + ytd_w))

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
        print(f"{ticker:<{ticker_w}}{'N/A':>{close_w}}{'N/A':>{ytd_w}}")
    elif latest_close == 'ERROR':
        print(f"{ticker:<{ticker_w}}{'ERROR':>{close_w}}{'N/A':>{ytd_w}}")
    else:
        print(f"{ticker:<{ticker_w}}{latest_close:>{close_w}.2f}{ytd_pct_change:>{ytd_w}.2f}%")




