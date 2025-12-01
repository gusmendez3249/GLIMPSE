import google.generativeai as genai
from app.core.config import Config
from app.core.logger import logger
from app.services.prompt_service import PromptService

class GeminiService:
    """Servicio para interactuar con Gemini AI"""
    
    def __init__(self):
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=Config.GEMINI_MODEL,
                generation_config=Config.GENERATION_CONFIG,
                safety_settings=Config.SAFETY_SETTINGS
            )
            logger.info("Gemini Service inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando Gemini: {str(e)}")
            raise
    
    def analyze_image(self, image, mode='detailed', custom_prompt=None):
        """
        Analiza una imagen usando Gemini
        
        Args:
            image: Objeto PIL Image
            mode: Modo de análisis (quick, detailed, code, document, creative)
            custom_prompt: Prompt personalizado (opcional)
        
        Returns:
            str: Respuesta del análisis
        """
        try:
            # Seleccionar prompt
            if custom_prompt:
                prompt = custom_prompt
                logger.info("Usando prompt personalizado")
            else:
                prompt = PromptService.get_prompt(mode)
                logger.info(f"Usando modo: {mode}")
            
            # Generar contenido
            logger.info("Enviando petición a Gemini...")
            response = self.model.generate_content([prompt, image])

            logger.info("Respuesta recibida exitosamente")

            # Manejar respuestas con múltiples partes
            try:
                return response.text
            except ValueError:
                # Si no hay .text, extraer de las partes
                if response.candidates and len(response.candidates) > 0:
                    parts = response.candidates[0].content.parts
                    return ''.join(part.text for part in parts if hasattr(part, 'text'))
                raise Exception("No se pudo extraer texto de la respuesta")
            
        except Exception as e:
            logger.error(f"Error en análisis Gemini: {str(e)}")
            raise Exception(f"Error al analizar imagen: {str(e)}")

# Instancia global
gemini_service = GeminiService()