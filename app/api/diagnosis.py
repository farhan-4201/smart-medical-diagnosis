"""
Medical diagnosis endpoints
"""
import os
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
from app.models.schemas import DiagnosisResponse, AudioResponse
from app.services.ai_service import ai_service
from app.services.audio_service import audio_service
from app.services.file_service import file_service
from app.core.exceptions import create_http_exception

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/diagnosis", tags=["diagnosis"])

@router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_image(
    file: UploadFile = File(..., description="Medical image to analyze"),
    symptoms: Optional[str] = Form(None, description="Patient's described symptoms")
):
    """Analyze uploaded medical image with optional symptoms"""
    
    file_path = None
    try:
        # Save uploaded file
        file_path = file_service.save_uploaded_file(file)
        
        # Analyze image with AI
        diagnosis_text = ai_service.analyze_image_with_symptoms(file_path, symptoms)
        
        # Calculate confidence (simplified - in production, this would be from the model)
        confidence = 85.0 if symptoms else 75.0
        
        return DiagnosisResponse(
            diagnosis=diagnosis_text,
            confidence=confidence,
            solution=diagnosis_text,  # For now, using same text
            audio_available=True
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise create_http_exception(500, f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup uploaded file
        if file_path:
            file_service.cleanup_file(file_path)

@router.post("/audio-response")
async def get_audio_response(
    text: str = Form(..., description="Text to convert to speech")
):
    """Generate audio response from text"""
    
    audio_path = None
    try:
        # Generate audio
        audio_path = audio_service.text_to_speech(text)
        
        # Read audio file
        audio_bytes = audio_service.get_audio_as_bytes(audio_path)
        
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=response.mp3"}
        )
        
    except Exception as e:
        logger.error(f"Audio generation failed: {str(e)}")
        raise create_http_exception(500, f"Audio generation failed: {str(e)}")
    
    finally:
        # Cleanup audio file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe")
):
    """Transcribe uploaded audio file"""
    
    file_path = None
    try:
        # Save uploaded audio file
        file_path = file_service.save_uploaded_file(file)
        
        # Transcribe audio
        transcription = ai_service.transcribe_audio(file_path)
        
        return {"transcription": transcription}
        
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise create_http_exception(500, f"Transcription failed: {str(e)}")
    
    finally:
        # Cleanup uploaded file
        if file_path:
            file_service.cleanup_file(file_path)