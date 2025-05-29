from flask import Flask, render_template_string, request
import requests
import os
import time
import logging

app = Flask(__name__)

HTML = """
<!doctype html>
<title>YTD Analyzer</title>
<h1>YTD Analyzer</h1>
<form method="post" id="ytd-form" onsubmit="showSpinner()">
  Tickers (comma separated): <input name="tickers" value="{{ tickers }}"><br>
  <input type="submit" value="Analyze" id="analyze-btn">
</form>
<div id="spinner" style="display:none;font-size:2em;">⏳ Processing...</div>
<pre>{{ results }}</pre>
<script>
function showSpinner() {
    document.getElementById('analyze-btn').disabled = true;
    document.getElementById('spinner').style.display = 'block';
}
</script>
"""

# Set up logging (at the top of your file, after imports)
logging.basicConfig(level=logging.INFO)

def get_ticker_list(tickers_str):
    return [t.strip().upper() 
            for t in tickers_str.split(",") if t.strip()]

def fetch_ytd_data(
        ticker, 
        total_timeout=10, 
        single_attempt_timeout=10):
    
    start_time = time.time()
    while time.time() - start_time < total_timeout:
        try:
            logging.info(f"Requesting YTD data for {ticker}")
            resp = requests.get(
                "https://pythonapptickets.onrender.com/ytd",
                params={"ticker": ticker},
                timeout=single_attempt_timeout
            )
            logging.info(f"Response for {ticker}: status={resp.status_code}, body={resp.text}")
            if resp.status_code == 200:
                data = resp.json()
                return (ticker, data['close'], data['ytd_pct_change'])
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
        time.sleep(1)
    return (ticker, "ERROR", None)

def sort_and_format_results(data_list):
    results = ""
    # Sort by ytd_pct_change descending, handling None and "ERROR"
    data_list.sort(key=lambda x: 
                   (isinstance(x[2], (int, float)),
                     x[2] if isinstance(x[2], (int, float)) 
                          else float('-inf')),
                            reverse=True)
    for ticker, close, ytd_pct_change in data_list:
        if close == "ERROR":
            results += f"{ticker}: ERROR\n"
        elif close is None:
            results += f"{ticker}: N/A\n"
        else:
            results += f"{ticker}: Close={close:.2f}, YTD % Change={ytd_pct_change:.2f}%\n"
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    default_tickers = "MSFT,AAPL,MSTR"
    results = ""
    tickers = default_tickers
    data_list = []
    if request.method == "POST":
        tickers = request.form["tickers"]
        ticker_list = get_ticker_list(tickers)
        for ticker in ticker_list:
            data_list.append(fetch_ytd_data(ticker))
        results = sort_and_format_results(data_list)
    return render_template_string(HTML, results=results, tickers=tickers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)