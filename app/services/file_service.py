"""
File handling services
"""
import os
import uuid
import logging
from typing import Optional, Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileProcessingError

logger = logging.getLogger(__name__)

class FileService:
    """Service for file upload and management"""
    
    def __init__(self):
        os.makedirs(settings.upload_dir, exist_ok=True)
    
    def save_uploaded_file(self, file: UploadFile) -> str:
        """Save uploaded file and return the file path"""
        try:
            # Validate file
            self._validate_file(file)
            
            # Generate unique filename
            file_extension = self._get_file_extension(file.filename)
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.upload_dir, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
            
            logger.info(f"File saved: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            raise FileProcessingError(f"Failed to save file: {str(e)}")
    
    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file.filename:
            raise FileProcessingError("No file provided")
        
        # Check file extension
        file_extension = self._get_file_extension(file.filename)
        if file_extension.lower() not in settings.allowed_extensions:
            raise FileProcessingError(
                f"File type not allowed. Supported formats: {', '.join(settings.allowed_extensions)}"
            )
        
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.max_file_size:
            raise FileProcessingError(
                f"File too large. Maximum size: {settings.max_file_size / (1024*1024):.1f}MB"
            )
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        return os.path.splitext(filename)[1]
    
    def cleanup_file(self, file_path: str) -> None:
        """Remove file from filesystem"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> None:
        """Clean up old uploaded files"""
        try:
            import time
            current_time = time.time()
            
            for filename in os.listdir(settings.upload_dir):
                file_path = os.path.join(settings.upload_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > (max_age_hours * 3600):
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup old files: {str(e)}")

# Global file service instance
file_service = FileService()