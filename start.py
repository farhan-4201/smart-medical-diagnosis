#!/usr/bin/env python3
"""
Simple startup script for AI Doctor
"""

if __name__ == "__main__":
    try:
        import uvicorn
        print("Starting AI Doctor on http://localhost:8000")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("Please install dependencies: pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\nServer stopped")