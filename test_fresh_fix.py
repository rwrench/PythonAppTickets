#!/usr/bin/env python3
"""
Quick test to demonstrate the fresh price fix works
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'web_app'))

from utils_fresh import fetch_ytd_data_direct, process_ticker_form

def test_fresh_data_fix():
    print("Testing Fresh Price Data Fix")
    print("=" * 50)
    
    test_tickers = "AAPL,MSFT"
    
    print(f"Testing tickers: {test_tickers}")
    print(f"Using direct fetch (bypasses API)")
    print("-" * 30)
    
    # Test the fixed function
    results = process_ticker_form(test_tickers, 5, use_direct_fetch=True)
    
    print("Results:")
    print(results)
    
    print("\n" + "=" * 50)
    print("✅ Fresh price fix demonstration complete!")
    print("\nTo use this fix in your application:")
    print("1. Run: python web_app_fresh.py")
    print("2. Open browser to http://localhost:5001")
    print("3. Check 'Use direct fetch' option")
    print("4. Enter tickers and click 'Analyze Fresh Data'")

if __name__ == "__main__":
    test_fresh_data_fix()
