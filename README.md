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

## Render Deployment

### Deploying to [Render](https://render.com):

- **requirements.txt:**  
  Ensure each service (`api_app` and `web_app`) has its own `requirements.txt` in its root directory.

- **Root Directory:**  
  In Render, set the "Root Directory" for each service to the appropriate subfolder (`api_app/` or `web_app/`).

- **Build Command:**  
  ```
  pip install -r requirements.txt
  ```

- **Start Command:**  
  For the API (FastAPI):
  ```
  uvicorn api_server:app --host 0.0.0.0 --port 10000
  ```
  For the Web App:
  ```
  python -m web_app.web_app
  ```

- **Environment Variables:**  
  Set any required environment variables (such as `YTD_API_URL`) in the Render dashboard for each service.

- **Access:**  
  After deployment, use the URLs provided by Render to access your API and web app.

---

**Note:**  
- Ensure you have all dependencies installed from `requirements.txt` in each app's directory.
- FastAPI is now used for the API server. Interactive docs are available at `/docs` when running locally or on Render.
