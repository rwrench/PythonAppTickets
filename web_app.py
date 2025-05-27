from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML = """
<!doctype html>
<title>YTD Analyzer</title>
<h1>YTD Analyzer</h1>
<form method="post">
  Tickers (comma separated): <input name="tickers" value="{{ tickers }}"><br>
  <input type="submit" value="Analyze">
</form>
<pre>{{ results }}</pre>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    default_tickers = "MSFT,AAPL,MSTR"
    results = ""
    tickers = default_tickers
    data_list = []
    if request.method == "POST":
        tickers = request.form["tickers"]
        ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
        for ticker in ticker_list:
            try:
                resp = requests.get("https://pythonapptickets.onrender.com/ytd", params={"ticker": ticker})
                if resp.status_code == 200:
                    data = resp.json()
                    # Store as (ticker, close, ytd_pct_change)
                    data_list.append((ticker, data['close'], data['ytd_pct_change']))
                else:
                    data_list.append((ticker, None, None))
            except Exception:
                data_list.append((ticker, "ERROR", None))
        # Sort by ytd_pct_change descending, handling None and "ERROR"
        data_list.sort(key=lambda x: (isinstance(x[2], (int, float)), x[2] if isinstance(x[2], (int, float)) else float('-inf')), reverse=True)
        for ticker, close, ytd_pct_change in data_list:
            if close == "ERROR":
                results += f"{ticker}: ERROR\n"
            elif close is None:
                results += f"{ticker}: N/A\n"
            else:
                results += f"{ticker}: Close={close:.2f}, YTD % Change={ytd_pct_change:.2f}%\n"
    return render_template_string(HTML, results=results, tickers=tickers)

if __name__ == "__main__":
    app.run(debug=True)