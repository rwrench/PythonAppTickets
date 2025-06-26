import yfinance as yf
import requests
import time
import logging
from datetime import datetime, timedelta
from config import API_URL  # Local import

def get_ticker_list(tickers_str):
    return [t.strip().upper() for t in tickers_str.split(",") if t.strip()]

def fetch_ytd_data_direct(ticker):
    """
    Fetch YTD data directly from yfinance with fresh data.
    This bypasses the API and ensures fresh prices.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        
        # Get real-time price first for most current data
        current_price = None
        try:
            fast_info = ticker_obj.fast_info
            if hasattr(fast_info, 'last_price') and fast_info.last_price:
                current_price = fast_info.last_price
        except:
            # Fallback to info if fast_info fails
            try:
                info = ticker_obj.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            except:
                pass
        
        # Get YTD historical data with extended date range
        today = datetime.now()
        start_of_year = f'{today.year}-01-01'
        end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Try multiple approaches to get the freshest data
        hist_data = None
        
        # Approach 1: Download with extended date range
        try:
            hist_data = yf.download(ticker, start=start_of_year, end=end_date, progress=False)
        except:
            pass
        
        # Approach 2: Use period="ytd" if download failed
        if hist_data is None or hist_data.empty:
            try:
                hist_data = ticker_obj.history(period="ytd", interval="1d")
            except:
                pass
        
        # Approach 3: Use recent history and extrapolate
        if hist_data is None or hist_data.empty:
            try:
                hist_data = ticker_obj.history(period="1y", interval="1d")
                # Filter to YTD
                if not hist_data.empty:
                    ytd_start = datetime(today.year, 1, 1)
                    hist_data = hist_data[hist_data.index >= ytd_start]
            except:
                pass
        
        if hist_data is not None and not hist_data.empty and 'Close' in hist_data.columns:
            ytd_open = float(hist_data['Close'].iloc[0])
            
            # Use current price if available and different, otherwise use latest close
            if current_price and abs(current_price - float(hist_data['Close'].iloc[-1])) > 0.01:
                latest_close = current_price
                logging.info(f"Using real-time price for {ticker}: ${current_price:.2f}")
            else:
                latest_close = float(hist_data['Close'].iloc[-1])
            
            ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
            
            # Log data freshness
            latest_date = hist_data.index[-1]
            logging.info(f"{ticker}: Latest data from {latest_date}, Close=${latest_close:.2f}, YTD={ytd_pct_change:.2f}%")
            
            return (ticker, latest_close, ytd_pct_change)
            
    except Exception as e:
        logging.error(f"Error fetching direct data for {ticker}: {e}")
    
    return (ticker, "ERROR", None)

def fetch_ytd_data(ticker, total_timeout=10, single_attempt_timeout=10, use_direct=False):
    """
    Fetch YTD data with option to use direct fetching or API.
    Set use_direct=True to bypass API and get fresh data directly.
    """
    if use_direct:
        return fetch_ytd_data_direct(ticker)
    
    # Original API-based fetching
    start_time = time.time()
    while time.time() - start_time < total_timeout:
        try:
            logging.info(f"Requesting YTD data for {ticker}")
            logging.info(f"API URL: {API_URL}")
            resp = requests.get(
                API_URL,
                params={"ticker": ticker},
                timeout=single_attempt_timeout,
                headers={
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            )
            logging.info(f"Response for {ticker}: status={resp.status_code}, body={resp.text}")
            if resp.status_code == 200:
                data = resp.json()
                return (ticker, data['close'], data['ytd_pct_change'])
            elif resp.status_code == 404:
                # Invalid ticker, don't retry
                logging.warning(f"Ticker {ticker} not found (404). Not retrying.")
                return (ticker, "ERROR", None)
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
        time.sleep(1)
    
    # If API fails, try direct as fallback
    logging.warning(f"API failed for {ticker}, trying direct fetch")
    return fetch_ytd_data_direct(ticker)

def sort_and_format_results(data_list):
    results = ""
    data_list.sort(key=lambda x: (isinstance(x[2], (int, float)), x[2] if isinstance(x[2], (int, float)) else float('-inf')), reverse=True)
    for ticker, close, ytd_pct_change in data_list:
        if close == "ERROR":
            results += f"{ticker}: ERROR\n"
        elif close is None:
            results += f"{ticker}: N/A\n"
        else:
            results += f"{ticker}: Close=${close:.2f}, YTD % Change={ytd_pct_change:.2f}%\n"
    return results

def process_ticker_form(tickers, max_tickers, use_direct_fetch=True):
    """
    Process ticker form with option to use direct fetching for fresh data.
    Set use_direct_fetch=True to bypass API and ensure fresh prices.
    """
    ticker_list = get_ticker_list(tickers)[:max_tickers]
    valid_data = []
    invalid_tickers = []
    
    for ticker in ticker_list:
        result = fetch_ytd_data(ticker, use_direct=use_direct_fetch)
        # result = (ticker, close, ytd_pct_change)
        if result[1] in ("ERROR", None):
            invalid_tickers.append(ticker)
        else:
            valid_data.append(result)
    
    if not valid_data:
        return "No valid tickers found. Please enter valid stock symbols."
    
    results = ""
    if invalid_tickers:
        results = f"Some tickers were invalid and ignored: {', '.join(invalid_tickers)}\n"
    
    # Add freshness indicator
    if use_direct_fetch:
        results += f"🔄 Using direct data fetch (bypasses API for fresh prices)\n"
    
    results += sort_and_format_results(valid_data)
    return results
