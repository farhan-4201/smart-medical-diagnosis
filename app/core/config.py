"""
Application configuration settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "AI Doctor"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # API Keys
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # File Upload Configuration
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".webp"]
    upload_dir: str = "uploads"
    
    # Audio Configuration
    max_recording_duration: int = 30  # seconds
    audio_format: str = "mp3"
    
    # Model Configuration
    vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    stt_model: str = "whisper-large-v3"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()