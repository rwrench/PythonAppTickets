import yfinance as yf
import pandas as pd
import asyncio

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

async def fetch_close_prices_async(ticker, start, end):
    return await asyncio.to_thread(fetch_close_prices, ticker, start, end)