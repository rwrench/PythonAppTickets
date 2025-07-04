#!/bin/bash

# Start API Server on macOS
echo "🚀 Starting FastAPI Server on macOS"
echo "===================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
fi

# Navigate to API directory
cd api_app

echo "📍 Starting API server on http://localhost:10000"
echo "📖 API docs will be available at http://localhost:10000/docs"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn api_server:app --host 0.0.0.0 --port 10000 --reload
