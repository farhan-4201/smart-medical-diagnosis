#!/usr/bin/env python3
"""
AI Doctor 2.0 - Application Runner
Enhanced startup script with comprehensive checks
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'groq',
        'gtts',
        'pydantic_settings',
        'jinja2',
        'python_multipart',
        'pillow',
        'aiofiles'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Install them with: pip install -r requirements.txt")
        return False
    
    logger.info("All required packages are installed")
    return True

def check_environment():
    """Check environment configuration"""
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        logger.error("GROQ_API_KEY not configured properly")
        logger.info("Please:")
        logger.info("1. Get your API key from: https://console.groq.com/")
        logger.info("2. Copy .env.example to .env")
        logger.info("3. Add your API key: GROQ_API_KEY=your_actual_key")
        return False
    
    logger.info("Environment configuration is valid")
    return True

def check_directories():
    """Create necessary directories"""
    directories = [
        "uploads",
        "app/static/images",
        "temp_audio",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Directory structure verified")
    return True

def test_groq_connection():
    """Test GROQ API connection"""
    try:
        from groq import Groq
        
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Test with a simple completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello, test connection"}],
            model="llama-3.1-8b-instant",
            max_tokens=10
        )
        
        logger.info("GROQ API connection successful")
        return True
        
    except Exception as e:
        logger.error(f"GROQ API connection failed: {str(e)}")
        return False

def run_application():
    """Start the FastAPI application"""
    try:
        import uvicorn
        from app.core.config import settings
        
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        logger.info(f"Server will be available at: http://{settings.host}:{settings.port}")
        logger.info("Press Ctrl+C to stop the server")
        
        uvicorn.run(
            "main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)

def main():
    """Main application runner"""
    print("🚀 AI Doctor 2.0 - Starting Application...\n")
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Directories", check_directories),
        ("GROQ Connection", test_groq_connection)
    ]
    
    for check_name, check_func in checks:
        print(f"🔍 Checking {check_name}...")
        if not check_func():
            print(f"❌ {check_name} check failed")
            sys.exit(1)
        print(f"✅ {check_name} check passed")
    
    print("\n🎉 All checks passed! Starting server...\n")
    
    # Start the application
    run_application()

if __name__ == "__main__":
    main()