"""
Custom exception classes
"""
from fastapi import HTTPException
from typing import Any, Dict, Optional

class AIDocterException(Exception):
    """Base exception for AI Doctor application"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class APIKeyError(AIDocterException):
    """Raised when API key is missing or invalid"""
    pass

class FileProcessingError(AIDocterException):
    """Raised when file processing fails"""
    pass

class ModelError(AIDocterException):
    """Raised when AI model processing fails"""
    pass

class AudioProcessingError(AIDocterException):
    """Raised when audio processing fails"""
    pass

def create_http_exception(
    status_code: int,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized HTTP exception"""
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "details": details or {},
            "status_code": status_code
        }
    )