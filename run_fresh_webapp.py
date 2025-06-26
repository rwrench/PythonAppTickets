#!/usr/bin/env python3
"""
Simple test script to run the fresh price web app with proper directory handling
"""

import os
import sys

# Add the web_app directory to Python path
web_app_dir = os.path.join(os.path.dirname(__file__), 'web_app')
sys.path.insert(0, web_app_dir)

# Change to web_app directory
os.chdir(web_app_dir)

print("Starting Fresh Price YTD Analyzer...")
print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {web_app_dir}")

try:
    # Import and run the Flask app
    from web_app_fresh import app
    
    print("✅ Successfully imported web app")
    print("🚀 Starting server on http://localhost:5001")
    print("💡 This version fetches real-time prices directly from Yahoo Finance")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5001, debug=True)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Checking available files...")
    print(os.listdir('.'))
    
except Exception as e:
    print(f"❌ Error starting web app: {e}")
    import traceback
    traceback.print_exc()
