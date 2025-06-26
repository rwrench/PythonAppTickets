#!/usr/bin/env python3
"""
Test the API server locally to ensure fresh price data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api_app'))

import asyncio
from api_server import ytd
from fastapi import HTTPException

async def test_api_locally():
    """Test the YTD API endpoint locally"""
    
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    print("Testing local API with improved price fetching")
    print("=" * 60)
    
    for ticker in test_tickers:
        print(f"\nTesting {ticker}:")
        try:
            response = await ytd(ticker)
            if hasattr(response, 'body'):
                # It's a JSONResponse
                import json
                data = json.loads(response.body)
            else:
                # It's a dict
                data = response
                
            print(f"  ✅ Close: ${data['close']:.2f}")
            print(f"  ✅ YTD Change: {data['ytd_pct_change']:.2f}%")
            if 'timestamp' in data:
                print(f"  ✅ Timestamp: {data['timestamp']}")
                
        except HTTPException as e:
            print(f"  ❌ HTTP Error {e.status_code}: {e.detail}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api_locally())
