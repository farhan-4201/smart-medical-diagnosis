"""
AI Doctor - Main FastAPI Application
Enhanced with proper structure and modern UI
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse

# Import application modules
from app.core.config import settings
from app.core.exceptions import create_http_exception
from app.api.health import router as health_router
from app.api.diagnosis import router as diagnosis_router
from app.services.file_service import file_service
from app.services.audio_service import audio_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Create necessary directories
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs("app/static/images", exist_ok=True)
    
    # Cleanup old files on startup
    file_service.cleanup_old_files()
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Doctor application")
    audio_service.cleanup_temp_files()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered medical diagnosis from skin images with voice support",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(health_router)
app.include_router(diagnosis_router)

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "app_name": settings.app_name},
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(exc)}")
    return templates.TemplateResponse(
        "500.html",
        {"request": request, "app_name": settings.app_name},
        status_code=500
    )

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "version": settings.app_version
        }
    )

@app.get("/health-check", response_class=HTMLResponse)
async def health_page(request: Request):
    """Health check page"""
    return templates.TemplateResponse(
        "health.html",
        {
            "request": request,
            "app_name": settings.app_name
        }
    )

# API Info endpoint
@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI-powered medical diagnosis API",
        "endpoints": {
            "health": "/health/",
            "diagnosis": "/api/diagnosis/analyze",
            "audio": "/api/diagnosis/audio-response",
            "transcribe": "/api/diagnosis/transcribe"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check if API key is configured
    if not settings.groq_api_key:
        logger.error("GROQ_API_KEY not configured. Please set it in your .env file")
        exit(1)
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )