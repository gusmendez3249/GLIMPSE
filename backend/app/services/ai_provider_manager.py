from app.core.config import Config
from app.core.logger import logger

class AIProviderManager:
    """Manager para manejar múltiples proveedores de IA con fallback"""
    
    def __init__(self):
        self.providers = []
        self.primary_provider = Config.PRIMARY_AI_PROVIDER
        
        # Intentar inicializar servicios según disponibilidad
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Inicializa los proveedores disponibles"""
        
        # Inicializar Claude si hay API key
        if Config.CLAUDE_API_KEY:
            try:
                from app.services.claude_service import claude_service
                self.providers.append(('claude', claude_service))
                logger.info("✓ Claude Service disponible")
            except Exception as e:
                logger.warning(f"⚠ Claude no disponible: {str(e)}")
        
        # Inicializar Groq si hay API key
        if Config.GROQ_API_KEY:
            try:
                from app.services.groq_service import groq_service
                self.providers.append(('groq', groq_service))
                logger.info("✓ Groq Service disponible")
            except Exception as e:
                logger.warning(f"⚠ Groq no disponible: {str(e)}")
        
        if not self.providers:
            raise Exception("No hay proveedores de IA disponibles. Verifica tus API keys.")
        
        # Ordenar para que el primario esté primero
        self.providers.sort(key=lambda x: 0 if x[0] == self.primary_provider else 1)
        logger.info(f"Proveedores inicializados: {[p[0] for p in self.providers]}")
    
    def analyze_image(self, image, mode='detailed', custom_prompt=None):
        """
        Analiza una imagen con fallback automático entre proveedores
        
        Args:
            image: Objeto PIL Image
            mode: Modo de análisis
            custom_prompt: Prompt personalizado (opcional)
        
        Returns:
            str: Respuesta del análisis
        """
        last_error = None
        
        for provider_name, provider_service in self.providers:
            try:
                logger.info(f"Intentando análisis con {provider_name}...")
                result = provider_service.analyze_image(image, mode, custom_prompt)
                logger.info(f"✓ Análisis exitoso con {provider_name}")
                return result
                
            except Exception as e:
                logger.warning(f"✗ Error con {provider_name}: {str(e)}")
                last_error = e
                
                # Si hay más proveedores, intentar con el siguiente
                if provider_name != self.providers[-1][0]:
                    logger.info(f"Intentando con fallback...")
                    continue
        
        # Si llegamos aquí, todos los proveedores fallaron
        raise Exception(f"Todos los proveedores fallaron. Último error: {str(last_error)}")

# Instancia global
ai_provider_manager = AIProviderManager()
