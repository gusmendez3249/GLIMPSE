import anthropic
import base64
from io import BytesIO
from app.core.config import Config
from app.core.logger import logger
from app.services.prompt_service import PromptService

class ClaudeService:
    """Servicio para interactuar con Claude AI - Vision"""
    
    def __init__(self):
        self.client = None
        self.model = None
        self._initialized = False
    
    def _ensure_initialized(self):
        """Inicializa el servicio solo cuando se necesita"""
        if self._initialized:
            return
        
        if not Config.CLAUDE_API_KEY:
            raise Exception("CLAUDE_API_KEY no configurada")
        
        try:
            self.client = anthropic.Anthropic(api_key=Config.CLAUDE_API_KEY)
            self.model = Config.CLAUDE_MODEL
            self._initialized = True
            logger.info(f"Claude Service inicializado - Modelo: {self.model}")
        except Exception as e:
            logger.error(f"Error inicializando Claude: {str(e)}")
            raise
    
    def analyze_image(self, image, mode='detailed', custom_prompt=None):
        """
        Analiza una imagen usando Claude Vision
        
        Args:
            image: Objeto PIL Image
            mode: Modo de análisis (quick, detailed, code, document, exam, study)
            custom_prompt: Prompt personalizado (opcional)
        
        Returns:
            str: Respuesta del análisis
        """
        self._ensure_initialized()
        
        try:
            # Convertir imagen PIL a base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Seleccionar prompt
            if custom_prompt:
                prompt = custom_prompt
                logger.info("Usando prompt personalizado")
            else:
                prompt = PromptService.get_prompt(mode)
                logger.info(f"Usando modo: {mode}")
            
            # Crear mensaje para Claude
            logger.info("Enviando petición a Claude...")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=Config.CLAUDE_CONFIG['max_tokens'],
                temperature=Config.CLAUDE_CONFIG['temperature'],
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            logger.info("Respuesta recibida de Claude exitosamente")
            
            # Extraer texto de la respuesta
            response_text = message.content[0].text
            return response_text
            
        except Exception as e:
            logger.error(f"Error en análisis Claude: {str(e)}")
            raise Exception(f"Error al analizar imagen con Claude: {str(e)}")

# Instancia global
claude_service = ClaudeService()
