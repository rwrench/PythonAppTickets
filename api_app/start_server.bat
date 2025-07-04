@echo off
echo Starting FastAPI server...
python -m uvicorn api_server:app --host 0.0.0.0 --port 10000 --reload
pause
