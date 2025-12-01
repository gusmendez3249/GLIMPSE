import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración central de la aplicación"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Gemini
    GEMINI_MODEL = 'gemini-2.5-pro'
    GENERATION_CONFIG = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 20
    
    # Image Processing
    MAX_IMAGE_SIZE = (1920, 1080)
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validate(cls):
        """Valida que la configuración sea correcta"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no configurada en .env")
        return True