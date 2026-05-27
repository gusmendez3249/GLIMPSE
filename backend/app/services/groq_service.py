from groq import Groq
import base64
from io import BytesIO
from app.core.config import Config
from app.core.logger import logger
from app.services.prompt_service import PromptService

class GroqService:
    """Servicio para interactuar con Groq AI - Vision (Llama 3.2 Vision)"""
    
    def __init__(self):
        self.client = None
        self.model = None
        self._initialized = False
    
    def _ensure_initialized(self):
        """Inicializa el servicio solo cuando se necesita"""
        if self._initialized:
            return
        
        if not Config.GROQ_API_KEY:
            raise Exception("GROQ_API_KEY no configurada")
        
        try:
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = Config.GROQ_MODEL
            self._initialized = True
            logger.info(f"Groq Service inicializado - Modelo: {self.model}")
        except Exception as e:
            logger.error(f"Error inicializando Groq: {str(e)}")
            raise
    
    def analyze_image(self, image, mode='detailed', custom_prompt=None):
        """
        Analiza una imagen usando Groq Vision (Llama 3.2)
        
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
            
            # Crear mensaje para Groq
            logger.info("Enviando petición a Groq...")
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=Config.GROQ_CONFIG['temperature'],
                max_tokens=Config.GROQ_CONFIG['max_tokens']
            )
            
            logger.info("Respuesta recibida de Groq exitosamente")
            
            # Extraer texto de la respuesta
            response_text = chat_completion.choices[0].message.content
            return response_text
            
        except Exception as e:
            logger.error(f"Error en análisis Groq: {str(e)}")
            raise Exception(f"Error al analizar imagen con Groq: {str(e)}")

# Instancia global
groq_service = GroqService()
