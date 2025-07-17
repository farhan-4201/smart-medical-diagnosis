"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DiagnosisRequest(BaseModel):
    """Request model for diagnosis"""
    symptoms: Optional[str] = Field(None, description="Patient's described symptoms")
    additional_info: Optional[str] = Field(None, description="Additional patient information")

class DiagnosisResponse(BaseModel):
    """Response model for diagnosis results"""
    diagnosis: str = Field(..., description="AI diagnosis result")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    solution: str = Field(..., description="Recommended treatment/solution")
    timestamp: datetime = Field(default_factory=datetime.now)
    audio_available: bool = Field(False, description="Whether audio response is available")

class AudioResponse(BaseModel):
    """Response model for audio data"""
    audio_data: str = Field(..., description="Base64 encoded audio data")
    format: str = Field(default="mp3", description="Audio format")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")

class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.now)
    services: dict = Field(..., description="Service availability status")

class ErrorResponse(BaseModel):
    """Error response model"""
    message: str = Field(..., description="Error message")
    details: dict = Field(default_factory=dict, description="Error details")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.now)