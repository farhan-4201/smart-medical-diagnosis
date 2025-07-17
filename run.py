#!/usr/bin/env python3
"""
AI Doctor 2.0 - Simple Application Runner
Simplified startup script to avoid import conflicts
"""

def main():
    """Main application runner with minimal imports"""
    print("🚀 AI Doctor 2.0 - Starting Application...\n")
    
    try:
        # Import uvicorn here to avoid early import issues
        import uvicorn
        
        print("✅ Starting FastAPI server...")
        print("🌐 Server will be available at: http://localhost:8000")
        print("📱 Open your browser and navigate to the URL above")
        print("⏹️  Press Ctrl+C to stop the server\n")
        
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please install dependencies with: pip install -r requirements.txt")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())