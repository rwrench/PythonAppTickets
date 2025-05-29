from flask import Flask, render_template_string, request
import logging
from web_app.utils import process_ticker_form
from web_app.config import MAX_TICKERS

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

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def index():
    default_tickers = "MSFT,AAPL,MSTR"
    results = ""
    tickers = default_tickers
    if request.method == "POST":
        tickers = request.form["tickers"]
        results = process_ticker_form(tickers, MAX_TICKERS)
    return render_template_string(HTML, results=results, tickers=tickers)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)