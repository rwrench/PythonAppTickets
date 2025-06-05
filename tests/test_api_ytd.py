# This script tests the YTD API endpoint for valid 
# and invalid ticker inputs.
# It uses the requests library with retry logic to handle transient errors.
# and ensure robust testing.
# It is designed to be run in a test environment where the API is accessible.
# Ensure you have the requests library installed:   # pip install requests
# pip install requests      


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RENDER_API_URL = "https://pythonapptickets.onrender.com/api/stocks/ytd"

# Set up a session with retries
session = requests.Session()
retries = Retry(
    total=3,                # Total retry attempts
    backoff_factor=2,       # Wait 2s, 4s, 8s between retries
    status_forcelist=[502, 503, 504],  # Retry on these HTTP status codes
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

def test_ytd_api_valid_ticker():
    """
    Tests the YTD API endpoint with a valid ticker symbol.

    Sends a GET request to the API with the ticker 'MSFT' and asserts that:
    - The response status code is 200 (OK).
    - The response JSON contains 'MSFT' either as a key or as the value of the 'ticker' field.
    """
    response = session.get(f"{RENDER_API_URL}?ticker=MSFT", timeout=(10, 90))
    assert response.status_code == 200
    data = response.json()
    assert "MSFT" in data or data.get("ticker") == "MSFT"

def test_ytd_api_invalid_ticker():
    response = session.get(f"{RENDER_API_URL}?ticker=INVALID", timeout=(10, 90))
    assert response.status_code == 400 # Or whatever your API returns
    data = response.json()
    assert data.get("detail") == "Invalid ticker format" or data.get("detail") == "Missing ticker"