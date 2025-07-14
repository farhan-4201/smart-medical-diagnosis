#!/usr/bin/env python3
"""
Backend runner script with proper error handling
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'groq',
        'gtts',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_api_key():
    """Check if GROQ API key is configured"""
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not configured properly")
        print("Please:")
        print("1. Get your API key from: https://console.groq.com/")
        print("2. Add it to your .env file: GROQ_API_KEY=your_actual_key")
        return False
    
    return True

def main():
    """Run the backend server with checks"""
    print("🚀 Starting AI Doctor Backend Server...")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # Start the server
    try:
        import uvicorn
        print("✅ All checks passed. Starting server on http://localhost:8000")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print(f"❌ Failed to start server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()