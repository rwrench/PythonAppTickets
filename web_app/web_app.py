from flask import Flask, render_template_string, request
import logging
from web_app.utils import process_ticker_form
from web_app.config import MAX_TICKERS

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
  <head>
    <title>YTD Analyzer</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h1 class="mb-4">YTD Analyzer</h1>
      <form method="post" id="ytd-form" onsubmit="showSpinner()" class="mb-4">
        <div class="mb-3">
          <label for="tickers" class="form-label">Tickers (comma separated):</label>
          <input name="tickers" id="tickers" class="form-control" value="{{ tickers }}">
        </div>
        <button type="submit" class="btn btn-primary" id="analyze-btn">Analyze</button>
      </form>
      <div id="spinner" style="display:none;font-size:2em;">⏳ Processing...</div>
      <pre class="mt-4 bg-white p-3 rounded border">{{ results }}</pre>
    </div>
    <script>
    function showSpinner() {
        document.getElementById('analyze-btn').disabled = true;
        document.getElementById('spinner').style.display = 'block';
    }
    </script>
  </body>
</html>
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