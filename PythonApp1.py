import yfinance as yf
import pandas as pd 
from datetime import datetime

def fetch_close_prices(ticker, start, end):
    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False
    )
    if not data.empty and 'Close' in data:
        close = data['Close']
        if isinstance(close, pd.DataFrame):
            if ticker in close.columns:
                close = close[ticker]
            else:
                return None
        if len(close) > 1:
            return close
    return None

def calculate_ytd_change(close):
    ytd_open = float(close.iloc[0])
    latest_close = float(close.iloc[-1])
    ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
    return latest_close, ytd_pct_change

def format_result(ticker, latest_close, ytd_pct_change, ticker_w=8, close_w=12, ytd_w=16):
    if latest_close is None:
        return f"{ticker:<{ticker_w}}{'N/A':>{close_w}}{'N/A':>{ytd_w}}"
    elif latest_close == 'ERROR':
        return f"{ticker:<{ticker_w}}{'ERROR':>{close_w}}{'N/A':>{ytd_w}}"
    else:
        return f"{ticker:<{ticker_w}}{latest_close:>{close_w}.2f}{ytd_pct_change:>{ytd_w}.2f}%"

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
        close = fetch_close_prices(ticker, start_of_year, today)
        if close is not None:
            latest_close, ytd_pct_change = calculate_ytd_change(close)
            results.append((ticker, latest_close, ytd_pct_change))
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
    print(format_result(ticker, latest_close, ytd_pct_change, ticker_w, close_w, ytd_w))




