#!/usr/bin/env python3

# Simple test to check if we can import and run uvicorn
import sys
import os

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Current working directory:", os.getcwd())

try:
    import uvicorn
    print("✓ uvicorn imported successfully")
except ImportError as e:
    print("✗ Failed to import uvicorn:", e)
    sys.exit(1)

try:
    import fastapi
    print("✓ fastapi imported successfully")
except ImportError as e:
    print("✗ Failed to import fastapi:", e)
    sys.exit(1)

try:
    from api_server import app
    print("✓ api_server imported successfully")
except ImportError as e:
    print("✗ Failed to import api_server:", e)
    print("Make sure you're in the correct directory and all dependencies are installed")
    sys.exit(1)

print("\nAll imports successful! You can now run:")
print("python -m uvicorn api_server:app --host 0.0.0.0 --port 10000")
