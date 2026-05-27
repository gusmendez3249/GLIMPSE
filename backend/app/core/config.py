import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración central de la aplicación"""
    
    # API Keys - Multi-Provider
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    PRIMARY_AI_PROVIDER = os.getenv('PRIMARY_AI_PROVIDER', 'claude')  # claude o groq
    
    # Flask
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Claude
    CLAUDE_MODEL = 'claude-opus-4-5'  # Modelo más potente disponible
    CLAUDE_CONFIG = {
        "max_tokens": 2048,
        "temperature": 1.0,  # Aumentado para más variabilidad
    }
    
    # Groq
    GROQ_MODEL = 'llama-3.2-11b-vision-preview'  # Modelo activo
    GROQ_CONFIG = {
        "max_tokens": 2048,
        "temperature": 0.7,
    }
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 20
    
    # Image Processing
    MAX_IMAGE_SIZE = (1920, 1080)
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validate(cls):
        """Valida que la configuración sea correcta"""
        if not cls.CLAUDE_API_KEY and not cls.GROQ_API_KEY:
            raise ValueError("Se requiere al menos CLAUDE_API_KEY o GROQ_API_KEY en .env")
        
        if cls.PRIMARY_AI_PROVIDER not in ['claude', 'groq']:
            raise ValueError("PRIMARY_AI_PROVIDER debe ser 'claude' o 'groq'")
        
        return True