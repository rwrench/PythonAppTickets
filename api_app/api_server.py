import logging
from flask import Flask, request, jsonify
from finance_utils import fetch_close_prices, calculate_ytd_change
from datetime import datetime
import re
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/ytd", methods=["GET"])
async def ytd():
    ticker = request.args.get("ticker")
    logging.info(f"Received /ytd request for ticker: {ticker}")
    if not ticker:
        logging.warning("Missing ticker parameter")
        return jsonify({"error": "Missing ticker"}), 400
    if not re.match(r"^[A-Z0-9]{1,5}$", ticker):
        logging.warning(f"Invalid ticker format: {ticker}")
        return jsonify({"error": "Invalid ticker format"}), 400
    today = datetime.today().strftime('%Y-%m-%d')
    start_of_year = f'{datetime.today().year}-01-01'
    try:
        close = await asyncio.to_thread(fetch_close_prices, ticker, start_of_year, today)
        if close is not None:
            latest_close, ytd_pct_change = calculate_ytd_change(close)
            logging.info(f"Returning data for {ticker}: close={latest_close}, ytd_pct_change={ytd_pct_change}")
            return jsonify({
                "ticker": ticker,
                "close": latest_close,
                "ytd_pct_change": ytd_pct_change
            })
        else:
            logging.warning(f"No data found for ticker: {ticker}")
            return jsonify({"error": "No data"}), 404
    except Exception as e:
        logging.error(f"Error processing ticker {ticker}: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)