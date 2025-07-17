"""
Audio processing services
"""
import os
import logging
from typing import Optional
from gtts import gTTS
from app.core.config import settings
from app.core.exceptions import AudioProcessingError

logger = logging.getLogger(__name__)

class AudioService:
    """Service for audio processing and text-to-speech"""
    
    def __init__(self):
        self.temp_dir = "temp_audio"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """Convert text to speech using gTTS"""
        try:
            if not output_path:
                output_path = os.path.join(self.temp_dir, "response.mp3")
            
            # Clean text for better speech synthesis
            cleaned_text = self._clean_text_for_speech(text)
            
            tts = gTTS(
                text=cleaned_text,
                lang="en",
                slow=False,
                tld="com"  # Use .com domain for better quality
            )
            
            tts.save(output_path)
            logger.info(f"Audio saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Text-to-speech failed: {str(e)}")
            raise AudioProcessingError(f"Failed to generate audio: {str(e)}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for better speech synthesis"""
        # Remove markdown formatting
        text = text.replace("**", "").replace("*", "")
        text = text.replace("_", "").replace("`", "")
        
        # Replace medical abbreviations with full words
        replacements = {
            "Dr.": "Doctor",
            "mg": "milligrams",
            "ml": "milliliters",
            "etc.": "etcetera",
            "i.e.": "that is",
            "e.g.": "for example"
        }
        
        for abbrev, full in replacements.items():
            text = text.replace(abbrev, full)
        
        return text
    
    def get_audio_as_bytes(self, audio_path: str) -> bytes:
        """Read audio file and return as bytes"""
        try:
            with open(audio_path, "rb") as audio_file:
                return audio_file.read()
        except Exception as e:
            logger.error(f"Failed to read audio file {audio_path}: {str(e)}")
            raise AudioProcessingError(f"Failed to read audio file: {str(e)}")
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp files: {str(e)}")

# Global audio service instance
audio_service = AudioService()