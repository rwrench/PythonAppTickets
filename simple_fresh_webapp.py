#!/usr/bin/env python3
"""
Simple standalone web app with fresh price data - no complex imports
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template_string, request
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def get_fresh_stock_data(ticker):
    """Get fresh stock data directly from yfinance"""
    try:
        ticker_obj = yf.Ticker(ticker)
        
        # Get real-time price
        current_price = None
        try:
            fast_info = ticker_obj.fast_info
            current_price = fast_info.last_price
        except:
            try:
                info = ticker_obj.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            except:
                pass
        
        # Get YTD data with extended date range
        today = datetime.now()
        start_of_year = f'{today.year}-01-01'
        end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Try multiple approaches for fresh data
        hist_data = None
        try:
            hist_data = yf.download(ticker, start=start_of_year, end=end_date, progress=False)
        except:
            try:
                hist_data = ticker_obj.history(period="ytd", interval="1d")
            except:
                try:
                    hist_data = ticker_obj.history(period="1y", interval="1d")
                    if not hist_data.empty:
                        ytd_start = datetime(today.year, 1, 1)
                        hist_data = hist_data[hist_data.index >= ytd_start]
                except:
                    pass
        
        if hist_data is not None and not hist_data.empty and 'Close' in hist_data.columns:
            ytd_open = float(hist_data['Close'].iloc[0])
            
            # Use current price if available and different
            if current_price and abs(current_price - float(hist_data['Close'].iloc[-1])) > 0.01:
                latest_close = current_price
            else:
                latest_close = float(hist_data['Close'].iloc[-1])
            
            ytd_pct_change = ((latest_close - ytd_open) / ytd_open) * 100
            
            latest_date = hist_data.index[-1]
            return {
                'ticker': ticker,
                'close': latest_close,
                'ytd_change': ytd_pct_change,
                'date': latest_date.strftime('%Y-%m-%d'),
                'success': True
            }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
    
    return {'ticker': ticker, 'success': False, 'error': 'Could not fetch data'}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fresh Stock Price Analyzer 📈</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="text-center mb-4">📈 Fresh Stock Price Analyzer</h1>
                
                <div class="alert alert-success" role="alert">
                    <strong>🔄 Real-time Data:</strong> This app fetches fresh prices directly from Yahoo Finance, bypassing any cached data.
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <form method="post" id="stock-form">
                            <div class="mb-3">
                                <label for="tickers" class="form-label">Stock Tickers (comma-separated):</label>
                                <input type="text" class="form-control" id="tickers" name="tickers" 
                                       value="{{ tickers }}" placeholder="AAPL,MSFT,MSTR,TSLA" required>
                                <div class="form-text">Enter up to 5 stock symbols separated by commas</div>
                            </div>
                            <button type="submit" class="btn btn-primary">Get Fresh Prices 🚀</button>
                        </form>
                    </div>
                </div>
                
                {% if results %}
                <div class="card mt-4">
                    <div class="card-header">
                        <h5>📊 Results (YTD Performance)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Ticker</th>
                                        <th>Current Price</th>
                                        <th>YTD Change</th>
                                        <th>Last Updated</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for result in results %}
                                    <tr>
                                        <td><strong>{{ result.ticker }}</strong></td>
                                        {% if result.success %}
                                        <td>${{ "%.2f"|format(result.close) }}</td>
                                        <td>
                                            <span class="badge {% if result.ytd_change >= 0 %}bg-success{% else %}bg-danger{% endif %}">
                                                {{ "%.2f"|format(result.ytd_change) }}%
                                            </span>
                                        </td>
                                        <td>{{ result.date }}</td>
                                        <td><span class="badge bg-success">✅ Fresh</span></td>
                                        {% else %}
                                        <td colspan="3">{{ result.error }}</td>
                                        <td><span class="badge bg-danger">❌ Error</span></td>
                                        {% endif %}
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <div class="text-center mt-4">
                    <small class="text-muted">
                        Data fetched on {{ current_time }}
                    </small>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tickers = "AAPL,MSFT,MSTR"
    results = []
    
    if request.method == 'POST':
        tickers_input = request.form.get('tickers', '').strip()
        if tickers_input:
            tickers = tickers_input
            ticker_list = [t.strip().upper() for t in tickers.split(',') if t.strip()][:5]  # Limit to 5
            
            for ticker in ticker_list:
                result = get_fresh_stock_data(ticker)
                results.append(result)
    
    return render_template_string(
        HTML_TEMPLATE, 
        tickers=tickers, 
        results=results,
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

if __name__ == '__main__':
    print("🚀 Starting Fresh Stock Price Analyzer")
    print("📍 Open your browser to: http://localhost:5001")
    print("💡 This version fetches real-time data directly from Yahoo Finance")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)  # Disable debug mode to avoid werkzeug issues
