#!/bin/bash

# Alternative download script for Mac Mini when git clone fails
echo "📥 Downloading Stock Ticker App from GitHub (Alternative Method)"
echo "=============================================================="

# Create project directory
mkdir -p ~/stock-ticker-app
cd ~/stock-ticker-app

# Download main files
echo "📄 Downloading main application files..."
curl -o simple_fresh_webapp.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/simple_fresh_webapp.py
curl -o README.md https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/README.md

# Download macOS scripts
echo "🍎 Downloading macOS deployment scripts..."
curl -o setup_macos.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/setup_macos.sh
curl -o start_simple_webapp_mac.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/start_simple_webapp_mac.sh
curl -o start_api_mac.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/start_api_mac.sh
curl -o start_webapp_mac.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/start_webapp_mac.sh
curl -o make_executable.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/make_executable.sh

# Create api_app directory and download files
echo "🔧 Downloading API files..."
mkdir -p api_app
cd api_app
curl -o api_server.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/api_app/api_server.py
curl -o finance_utils.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/api_app/finance_utils.py
curl -o requirements.txt https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/api_app/requirements.txt
cd ..

# Create web_app directory and download files
echo "🌐 Downloading web app files..."
mkdir -p web_app
cd web_app
curl -o web_app.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/web_app/web_app.py
curl -o utils.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/web_app/utils.py
curl -o config.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/web_app/config.py
curl -o requirements.txt https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/web_app/requirements.txt
curl -o __init__.py https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/web_app/__init__.py
cd ..

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x *.sh

echo ""
echo "✅ Download complete!"
echo "📁 Files downloaded to: $(pwd)"
echo ""
echo "🚀 Next steps:"
echo "1. Run: ./setup_macos.sh"
echo "2. Start app: ./start_simple_webapp_mac.sh"
echo ""
