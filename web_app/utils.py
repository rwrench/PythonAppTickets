import requests
import time
import logging
from web_app.config import API_URL

def get_ticker_list(tickers_str):
    return [t.strip().upper() for t in tickers_str.split(",") if t.strip()]

def fetch_ytd_data(ticker, total_timeout=10, single_attempt_timeout=10):
    start_time = time.time()
    while time.time() - start_time < total_timeout:
        try:
            logging.info(f"Requesting YTD data for {ticker}")
            logging.info(f"API URL: {API_URL}")
            resp = requests.get(
                API_URL,
                params={"ticker": ticker},
                timeout=single_attempt_timeout
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
    return (ticker, "ERROR", None)

def sort_and_format_results(data_list):
    results = ""
    data_list.sort(key=lambda x: (isinstance(x[2], (int, float)), x[2] if isinstance(x[2], (int, float)) else float('-inf')), reverse=True)
    for ticker, close, ytd_pct_change in data_list:
        if close == "ERROR":
            results += f"{ticker}: ERROR\n"
        elif close is None:
            results += f"{ticker}: N/A\n"
        else:
            results += f"{ticker}: Close={close:.2f}, YTD % Change={ytd_pct_change:.2f}%\n"
    return results



def process_ticker_form(tickers, max_tickers):
    ticker_list = get_ticker_list(tickers)[:max_tickers]
    valid_data = []
    invalid_tickers = []
    for ticker in ticker_list:
        result = fetch_ytd_data(ticker)
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
    results += sort_and_format_results(valid_data)
    return results