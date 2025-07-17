"""
AI processing services for image analysis and text generation
"""
import base64
import logging
from typing import Optional, Tuple
from groq import Groq
from app.core.config import settings
from app.core.exceptions import APIKeyError, ModelError

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered medical analysis"""
    
    def __init__(self):
        if not settings.groq_api_key:
            raise APIKeyError("GROQ API key is required")
        self.client = Groq(api_key=settings.groq_api_key)
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for medical analysis"""
        return """You are a professional medical AI assistant. Analyze the provided image and symptoms to provide helpful medical insights.

Guidelines:
- Provide clear, professional medical observations
- Suggest appropriate remedies or next steps
- Always recommend consulting a healthcare professional for serious concerns
- Keep responses concise but informative (2-3 sentences)
- Use empathetic, patient-friendly language
- Start responses with "Based on what I observe..." rather than "In the image I see"
- Avoid markdown formatting in responses

Remember: This is for educational purposes and should not replace professional medical advice."""

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 format"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {str(e)}")
            raise ModelError(f"Failed to process image: {str(e)}")

    def analyze_image_with_symptoms(
        self, 
        image_path: str, 
        symptoms: Optional[str] = None
    ) -> str:
        """Analyze image with optional symptom description"""
        try:
            encoded_image = self.encode_image(image_path)
            
            # Construct query with symptoms if provided
            query = self.system_prompt
            if symptoms:
                query += f"\n\nPatient's described symptoms: {symptoms}"
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}",
                            },
                        },
                    ],
                }
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=settings.vision_model,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            raise ModelError(f"Analysis failed: {str(e)}")

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using Groq Whisper"""
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=settings.stt_model,
                    file=audio_file,
                    language="en"
                )
            return transcription.text
        except Exception as e:
            logger.error(f"Audio transcription failed: {str(e)}")
            raise ModelError(f"Audio transcription failed: {str(e)}")

# Global AI service instance
ai_service = AIService()