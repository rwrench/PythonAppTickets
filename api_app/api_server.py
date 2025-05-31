import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from finance_utils import fetch_close_prices, calculate_ytd_change
from datetime import datetime
import re
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/ytd")
async def ytd(ticker: str = Query(..., description="Stock ticker symbol")):
    logging.info(f"Received /ytd request for ticker: {ticker}")
    if not ticker:
        logging.warning("Missing ticker parameter")
        raise HTTPException(status_code=400, detail="Missing ticker")
    if not re.match(r"^[A-Z0-9]{1,5}$", ticker):
        logging.warning(f"Invalid ticker format: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    today = datetime.today().strftime('%Y-%m-%d')
    start_of_year = f'{datetime.today().year}-01-01'
    try:
        close = await asyncio.to_thread(fetch_close_prices, ticker, start_of_year, today)
        if close is not None:
            latest_close, ytd_pct_change = calculate_ytd_change(close)
            logging.info(f"Returning data for {ticker}: close={latest_close}, ytd_pct_change={ytd_pct_change}")
            return {
                "ticker": ticker,
                "close": latest_close,
                "ytd_pct_change": ytd_pct_change
            }
        else:
            logging.warning(f"No data found for ticker: {ticker}")
            raise HTTPException(status_code=404, detail="No data")
    except Exception as e:
        logging.error(f"Error processing ticker {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# To run: uvicorn api_server:app --host 0.0.0.0 --port 10000