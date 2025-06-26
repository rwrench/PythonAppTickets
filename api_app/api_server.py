import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from finance_utils import fetch_close_prices, calculate_ytd_change, get_real_time_price
from datetime import datetime, timedelta
import re
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/api/stocks/ytd")
async def ytd(ticker: str = Query(..., description="Stock ticker symbol")):
    logging.info(f"Received /ytd request for ticker: {ticker}")
    if not ticker:
        logging.warning("Missing ticker parameter")
        raise HTTPException(status_code=400, detail="Missing ticker")
    if not re.match(r"^[A-Z0-9]{1,5}$", ticker):
        logging.warning(f"Invalid ticker format: {ticker}")
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    
    # Use current date/time to ensure fresh data
    today = datetime.now()
    start_of_year = f'{today.year}-01-01'
    
    # Use today + 1 day to ensure we capture current day's data
    end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        close = await asyncio.to_thread(fetch_close_prices, ticker, start_of_year, end_date)
        if close is not None and len(close) > 0:
            latest_close, ytd_pct_change = calculate_ytd_change(close)
            
            # Also try to get real-time price as a fallback/verification
            real_time_price = await asyncio.to_thread(get_real_time_price, ticker)
            
            # Use real-time price if it's more recent than our close data
            if real_time_price and abs(real_time_price - latest_close) > 0.01:
                logging.info(f"Using real-time price {real_time_price} vs historical {latest_close}")
                # Recalculate YTD change with real-time price
                ytd_open = float(close.iloc[0])
                ytd_pct_change = ((real_time_price - ytd_open) / ytd_open) * 100
                latest_close = real_time_price
            
            logging.info(f"Returning data for {ticker}: close={latest_close}, ytd_pct_change={ytd_pct_change}")
            
            # Return response with cache-busting headers
            response_data = {
                "ticker": ticker,
                "close": latest_close,
                "ytd_pct_change": ytd_pct_change,
                "timestamp": datetime.now().isoformat()
            }
            
            response = JSONResponse(content=response_data)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            
            return response
        else:
            logging.warning(f"No data found for ticker: {ticker}")
            raise HTTPException(status_code=404, detail="No data")
    except Exception as e:
        logging.error(f"Error processing ticker {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# To run: uvicorn api_server:app --host 0.0.0.0 --port 10000