"""
Health check endpoints
"""
from fastapi import APIRouter
from app.models.schemas import HealthCheck
from app.core.config import settings
from app.services.ai_service import ai_service

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    
    # Check service availability
    services = {
        "groq_api": bool(settings.groq_api_key),
        "ai_service": True,  # AI service is initialized
        "file_upload": True,
        "audio_processing": True
    }
    
    return HealthCheck(
        status="healthy" if all(services.values()) else "degraded",
        version=settings.app_version,
        services=services
    )