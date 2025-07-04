#!/bin/bash

# macOS Deployment Setup Script for Stock Ticker App
# Run this script on your Mac Mini to set up the environment

echo "🍎 Setting up Stock Ticker App on macOS"
echo "========================================"

# Check if Python 3.11+ is installed
echo "🐍 Checking Python version..."

# Try different Python commands
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found!"
    echo ""
    echo "📥 Please install Python 3.11+ using one of these methods:"
    echo "1. Download from: https://www.python.org/downloads/"
    echo "2. Install via Homebrew: brew install python@3.11"
    echo "3. Install via pyenv: pyenv install 3.11.9"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION using command: $PYTHON_CMD"

# Check if it's 3.11+
if $PYTHON_CMD -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "✅ Python version is compatible (3.11+)"
else
    echo "❌ Python 3.11+ required. Current version: $PYTHON_VERSION"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is available
echo "📦 Checking pip..."
if command -v pip3 &>/dev/null; then
    echo "✅ pip3 is available"
    PIP_CMD="pip3"
elif command -v pip &>/dev/null; then
    echo "✅ pip is available"
    PIP_CMD="pip"
else
    echo "❌ pip not found. Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
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
$PIP_CMD install -r requirements.txt
cd ..

# Install dependencies for web app
echo "📥 Installing web app dependencies..."
cd web_app
$PIP_CMD install -r requirements.txt
cd ..

# Install dependencies for simple fresh webapp
echo "📥 Installing simple webapp dependencies..."
$PIP_CMD install flask yfinance

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
