first python project to read stock ticker information 

## Testing Notes

### API (`api_app/api_server.py`)
- **Run locally:**  
  From the `api_app` directory, start the API server:
  ```
  python api_server.py
  ```
- **Test endpoint:**  
  Open your browser or use curl/Postman to test:
  ```
  http://localhost:10000/ytd?ticker=MSFT
  ```
  Replace `MSFT` with any ticker symbol.

### Web App (`web_app/web_app.py`)
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
  For the API:
  ```
  python api_server.py
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
- For async support, Flask 2.x+ and `flask[async]` are required.
