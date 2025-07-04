#!/bin/bash

# Start Web App on macOS
echo "🌐 Starting Flask Web App on macOS"
echo "=================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
fi

echo "📍 Starting web app on http://localhost:5000"
echo "⚠️  Make sure API server is running on port 10000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start the web app from project root
python -m web_app.web_app
