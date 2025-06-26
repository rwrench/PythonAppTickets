from flask import Flask, render_template_string, request
import logging
from web_app.utils_fresh import process_ticker_form  # Use fresh utils
from web_app.config import MAX_TICKERS

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
  <head>
    <title>YTD Analyzer - Fresh Prices ✨</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h1 class="mb-4">YTD Analyzer - Fresh Prices ✨</h1>
      <div class="alert alert-info">
        <strong>🔄 Fresh Data Mode:</strong> This version bypasses API caching and fetches real-time prices directly from Yahoo Finance.
      </div>
      <form method="post" id="ytd-form" onsubmit="showSpinner()" class="mb-4">
        <div class="mb-3">
          <label for="tickers" class="form-label">Tickers (comma separated):</label>
          <input name="tickers" id="tickers" class="form-control" value="{{ tickers }}" placeholder="AAPL,MSFT,MSTR">
        </div>
        <div class="mb-3 form-check">
          <input type="checkbox" class="form-check-input" id="use_direct" name="use_direct" checked>
          <label class="form-check-label" for="use_direct">
            Use direct fetch (recommended for fresh prices)
          </label>
        </div>
        <button type="submit" class="btn btn-primary" id="analyze-btn">Analyze Fresh Data</button>
      </form>
      <div id="spinner" style="display:none;font-size:2em;">⏳ Fetching fresh prices...</div>
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
        use_direct = 'use_direct' in request.form
        
        # Use fresh data fetching
        results = process_ticker_form(tickers, MAX_TICKERS, use_direct_fetch=use_direct)
        
    return render_template_string(HTML, results=results, tickers=tickers)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))  # Different port to avoid conflicts
    print(f"Starting Fresh Price YTD Analyzer on port {port}")
    print("This version fetches real-time prices directly from Yahoo Finance")
    app.run(host="0.0.0.0", port=port, debug=True)
