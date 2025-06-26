#!/bin/bash
# Deployment script for fresh price data fix

echo "🚀 Deploying Fresh Price Data Fix to GitHub/Render"
echo "=================================================="

echo "📋 Files being deployed:"
echo "✅ Modified: api_app/api_server.py (cache-busting, real-time data)"
echo "✅ Modified: api_app/finance_utils.py (enhanced price fetching)"
echo "✅ New: PRICE_FIX_GUIDE.md (complete documentation)"
echo "✅ New: simple_fresh_webapp.py (standalone web app)"
echo "✅ New: web_app/utils_fresh.py (fresh data utilities)"
echo "✅ New: test scripts for validation"

echo ""
echo "🔧 Staging all changes..."
git add .

echo ""
echo "📝 Committing with descriptive message..."
git commit -m "Fix stale price data issue

- Add real-time price fetching with yfinance fast_info
- Implement cache-busting headers in API
- Create enhanced web app with modern UI
- Add multiple fallback methods for data retrieval
- Include comprehensive documentation and tests

Fixes #4 - inconsistent ticket pricing by pulling current prices"

echo ""
echo "🚀 Pushing to GitHub (will trigger Render auto-deploy)..."
git push origin HEAD

echo ""
echo "✅ Deployment initiated!"
echo "🔍 Monitor Render dashboard for deployment status"
echo "🌐 Test API endpoint after deployment: https://pythonapptickets.onrender.com/api/stocks/ytd?ticker=AAPL"
echo "📱 Local fallback available: python simple_fresh_webapp.py"
