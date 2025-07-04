#!/bin/bash
# One-command Mac Mini setup for Stock Ticker App
# Usage: curl -s https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/quick_setup.sh | bash

echo "🚀 Quick Setup for Mac Mini"
echo "========================="

# Download and run the alternative download script
curl -s -o setup.sh https://raw.githubusercontent.com/rwrench/PythonAppTickets/master/download_for_mac.sh
chmod +x setup.sh
./setup.sh

echo ""
echo "✅ Setup complete!"
echo "📱 To start the app, run: ./start_simple_webapp_mac.sh"
