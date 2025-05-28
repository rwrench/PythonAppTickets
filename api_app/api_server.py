from flask import Flask, request, jsonify
from api_app.finance_utils import fetch_close_prices, calculate_ytd_change
from datetime import datetime

app = Flask(__name__)

@app.route("/ytd", methods=["GET"])
def ytd():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing ticker"}), 400
    today = datetime.today().strftime('%Y-%m-%d')
    start_of_year = f'{datetime.today().year}-01-01'
    close = fetch_close_prices(ticker, start_of_year, today)
    if close is not None:
        latest_close, ytd_pct_change = calculate_ytd_change(close)
        return jsonify({
            "ticker": ticker,
            "close": latest_close,
            "ytd_pct_change": ytd_pct_change
        })
    else:
        return jsonify({"error": "No data"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)