#!/bin/bash

# Make all shell scripts executable
echo "🔧 Making shell scripts executable..."

chmod +x setup_macos.sh
chmod +x start_api_mac.sh
chmod +x start_webapp_mac.sh
chmod +x start_simple_webapp_mac.sh
chmod +x deploy_fix.sh

echo "✅ All shell scripts are now executable"
echo ""
echo "🚀 Ready for macOS deployment!"
echo "Run ./setup_macos.sh to begin setup"
