#!/bin/bash

# Start Simple Fresh Web App on macOS
echo "📈 Starting Simple Fresh Stock Price Analyzer on macOS"
echo "====================================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
fi

echo "📍 Starting fresh stock analyzer on http://localhost:5001"
echo "🔄 This app fetches real-time data directly from Yahoo Finance"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start the simple fresh webapp
# Try different Python commands
if command -v python3 &>/dev/null; then
    python3 simple_fresh_webapp.py
elif command -v python &>/dev/null; then
    python simple_fresh_webapp.py
else
    echo "❌ Python not found! Please install Python 3.11+ first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi
