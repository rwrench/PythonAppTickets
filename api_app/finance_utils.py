import yfinance as yf
import pandas as pd
import asyncio
from datetime import datetime, timedelta

def fetch_close_prices(ticker, start, end):
    """
    Fetch close prices with enhanced data freshness.
    Uses multiple methods to ensure we get the most recent data.
    """
    try:
        # Method 1: Standard download with extended end date to ensure current data
        today = datetime.now()
        # Add one day to end date to ensure we capture today's data
        end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        
        data = yf.download(
            ticker,
            start=start,
            end=end_date,  # Use extended end date
            progress=False,
            auto_adjust=False
        )
        
        # If we don't have data or it's not recent enough, try period-based approach
        if data.empty or (not data.empty and len(data) == 0):
            print(f"Standard download empty, trying period-based approach for {ticker}")
            ticker_obj = yf.Ticker(ticker)
            data = ticker_obj.history(period="ytd", interval="1d", prepost=True)
        
        # Additional attempt with recent data if we still don't have enough
        if data.empty or len(data) < 5:  # If we have very little data
            print(f"Attempting to get more recent data for {ticker}")
            ticker_obj = yf.Ticker(ticker)
            recent_data = ticker_obj.history(period="1mo", interval="1d", prepost=True)
            if not recent_data.empty:
                # If recent_data has more or better data, use it
                if data.empty or len(recent_data) > len(data):
                    data = recent_data
        
        if not data.empty and 'Close' in data:
            close = data['Close']
            if isinstance(close, pd.DataFrame):
                if ticker in close.columns:
                    close = close[ticker]
                else:
                    return None
            if len(close) > 0:  # Changed from > 1 to > 0 to handle single-day data
                return close
                
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        
    return None

def calculate_ytd_change(close):
    """
    Calculate YTD change with better handling for current data.
    """
    if len(close) == 0:
        return None, None
    
    ytd_open = float(close.iloc[0])
    latest_close = float(close.iloc[-1])
    ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
    
    # Log the data freshness
    latest_date = close.index[-1]
    print(f"Latest data date: {latest_date}, Close: {latest_close}")
    
    return latest_close, ytd_pct_change

def get_real_time_price(ticker):
    """
    Get the most current price available using yfinance fast_info.
    Falls back to regular info if fast_info is not available.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        
        # Try fast_info first (faster and more current)
        try:
            fast_info = ticker_obj.fast_info
            if hasattr(fast_info, 'last_price') and fast_info.last_price:
                return fast_info.last_price
        except:
            pass
        
        # Fall back to info
        info = ticker_obj.info
        if 'currentPrice' in info and info['currentPrice']:
            return info['currentPrice']
        if 'regularMarketPrice' in info and info['regularMarketPrice']:
            return info['regularMarketPrice']
        if 'previousClose' in info and info['previousClose']:
            return info['previousClose']
            
    except Exception as e:
        print(f"Error getting real-time price for {ticker}: {e}")
    
    return None

async def fetch_close_prices_async(ticker, start, end):
    return await asyncio.to_thread(fetch_close_prices, ticker, start, end)