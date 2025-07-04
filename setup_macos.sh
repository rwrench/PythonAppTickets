#!/bin/bash

# macOS Deployment Setup Script for Stock Ticker App
# Run this script on your Mac Mini to set up the environment

echo "🍎 Setting up Stock Ticker App on macOS"
echo "========================================"

# Check if Python 3.11+ is installed
echo "🐍 Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Found Python $PYTHON_VERSION"
    
    # Check if it's 3.11+
    if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
        echo "✅ Python version is compatible (3.11+)"
    else
        echo "❌ Python 3.11+ required. Current version: $PYTHON_VERSION"
        echo "Please install Python 3.11+ from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "❌ Python3 not found. Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is available
echo "📦 Checking pip..."
if command -v pip3 &>/dev/null; then
    echo "✅ pip3 is available"
else
    echo "❌ pip3 not found. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies for API
echo "📥 Installing API dependencies..."
cd api_app
pip install -r requirements.txt
cd ..

# Install dependencies for web app
echo "📥 Installing web app dependencies..."
cd web_app
pip install -r requirements.txt
cd ..

# Install dependencies for simple fresh webapp
echo "📥 Installing simple webapp dependencies..."
pip install flask yfinance

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the applications:"
echo "1. API Server: ./start_api_mac.sh"
echo "2. Web App: ./start_webapp_mac.sh"
echo "3. Simple Fresh App: ./start_simple_webapp_mac.sh"
echo ""
echo "📱 Access URLs:"
echo "- API Docs: http://localhost:10000/docs"
echo "- Web App: http://localhost:5000"
echo "- Simple Fresh App: http://localhost:5001"
