#!/usr/bin/env python3
"""
Test the improved price fetching functionality to ensure we get fresh data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api_app'))

from finance_utils import fetch_close_prices, calculate_ytd_change, get_real_time_price
from datetime import datetime, timedelta

def test_price_freshness():
    ticker = 'AAPL'
    today = datetime.now()
    start_of_year = f'{today.year}-01-01'
    end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"Testing improved price fetching for {ticker}")
    print(f"Date range: {start_of_year} to {end_date}")
    print(f"Current time: {today}")
    print("-" * 50)
    
    # Test 1: Enhanced close prices
    print("1. Testing enhanced close prices...")
    close_data = fetch_close_prices(ticker, start_of_year, end_date)
    
    if close_data is not None:
        latest_close, ytd_pct_change = calculate_ytd_change(close_data)
        print(f"   Historical close: ${latest_close:.2f}")
        print(f"   YTD change: {ytd_pct_change:.2f}%")
        print(f"   Data points: {len(close_data)}")
        print(f"   Latest date: {close_data.index[-1]}")
    else:
        print("   ERROR: No close data found!")
        return
    
    # Test 2: Real-time price
    print("\n2. Testing real-time price...")
    real_time_price = get_real_time_price(ticker)
    
    if real_time_price:
        print(f"   Real-time price: ${real_time_price:.2f}")
        
        # Calculate difference
        if latest_close:
            diff = real_time_price - latest_close
            print(f"   Difference from historical: ${diff:.2f}")
            
            # Use real-time for YTD if different
            if abs(diff) > 0.01:  # More than 1 cent difference
                ytd_open = float(close_data.iloc[0])
                real_time_ytd = ((real_time_price - ytd_open) / ytd_open) * 100
                print(f"   Real-time YTD change: {real_time_ytd:.2f}%")
                print(f"   Recommendation: Use real-time price")
            else:
                print(f"   Prices match closely - historical data is current")
    else:
        print("   Could not fetch real-time price")
    
    # Test 3: Data freshness check
    print("\n3. Data freshness analysis...")
    if close_data is not None:
        latest_date = close_data.index[-1]
        
        # Remove timezone info for comparison if present
        if hasattr(latest_date, 'tz_localize'):
            latest_date_naive = latest_date.tz_localize(None) if latest_date.tz else latest_date
        else:
            latest_date_naive = latest_date
            
        today_naive = today.replace(tzinfo=None)
        days_old = (today_naive.date() - latest_date_naive.date()).days
        
        print(f"   Latest data date: {latest_date}")
        print(f"   Current date: {today.date()}")
        print(f"   Data age: {days_old} days")
        
        if days_old == 0:
            print("   ✅ Data is from TODAY - Very fresh!")
        elif days_old == 1 and today.hour < 16:  # Before market close
            print("   ✅ Data is from yesterday (market may not be open yet)")
        elif days_old <= 1:
            print("   ✅ Data is very recent")
        elif days_old <= 3:
            print("   ⚠️  Data is a few days old (weekend?)")
        else:
            print("   ❌ Data is stale - investigation needed")

if __name__ == "__main__":
    test_price_freshness()
