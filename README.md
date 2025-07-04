first python project to read stock ticker information 

## Requirements

- **Python 3.11.1** or higher

## Testing Notes

### API (`api_app/api_server.py`)
- **Install dependencies:**  
  From the `api_app` directory:
  ```
  pip install -r requirements.txt
  ```
- **Run locally (FastAPI):**  
  From the `api_app` directory, start the API server:
  ```
  uvicorn api_server:app --host 0.0.0.0 --port 10000
  ```
- **Interactive docs:**  
  Open your browser to:
  ```
  http://localhost:10000/docs
  ```
- **Test endpoint:**  
  Open your browser or use curl/Postman to test:
  ```
  http://localhost:10000/api/stocks/ytd?ticker=MSFT
  ```
  Replace `MSFT` with any ticker symbol.

### Web App (`web_app/web_app.py`)
- **Install dependencies:**  
  From the `web_app` directory:
  ```
  pip install -r requirements.txt
  ```
- **Run locally:**  
  From the project root, run:
  ```
  python -m web_app.web_app
  ```
- **Test in browser:**  
  Go to:
  ```
  http://localhost:5000/
  ```
  Enter one or more comma-separated tickers (e.g., `MSFT,AAPL,MSTR,INVALID`) and click "Analyze".

---

## Running Tests Locally

- **API tests:**  
  ```
  pytest tests/test_api_ytd.py
  ```
- **Selenium/web tests:**  
  ```
  pytest tests/test_webapp_selenium.py
  ```

---

## macOS Deployment (Mac Mini)

### Quick Setup
1. **Clone/copy the project** to your Mac Mini
2. **Make scripts executable:**
   ```bash
   chmod +x make_executable.sh && ./make_executable.sh
   ```
3. **Run setup:**
   ```bash
   ./setup_macos.sh
   ```

### Starting the Applications
- **API Server (port 10000):**
  ```bash
  ./start_api_mac.sh
  ```
- **Web App (port 5000):**
  ```bash
  ./start_webapp_mac.sh
  ```
- **Simple Fresh App (port 5001):**
  ```bash
  ./start_simple_webapp_mac.sh
  ```

### Access URLs
- API Documentation: `http://localhost:10000/docs`
- Web App: `http://localhost:5000`
- Simple Fresh App: `http://localhost:5001` (recommended - standalone)

---

## Network Access

To access your app from other devices on your network:

1. **Find your device's IP address:**
   - **Windows**: `ipconfig` 
   - **Mac**: `ifconfig | grep "inet " | grep -v 127.0.0.1`

2. **Access from other devices:**
   - Replace `localhost` with your IP address
   - Example: `http://192.168.1.100:5001`

---

**Note:**  
- Ensure you have all dependencies installed from `requirements.txt` in each app's directory.
- FastAPI is used for the API server. Interactive docs are available at `/docs` when running locally.
- The Simple Fresh App (port 5001) is recommended as it's standalone and doesn't require the API server.
