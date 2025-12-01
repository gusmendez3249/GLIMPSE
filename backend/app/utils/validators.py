from app.services.prompt_service import PromptService

class RequestValidator:
    """Validadores para requests de la API"""
    
    @staticmethod
    def validate_analyze_request(data):
        """Valida el request de análisis de imagen"""
        
        if not data:
            raise ValueError("Request vacío")
        
        if 'image' not in data:
            raise ValueError("Campo 'image' requerido")
        
        if not isinstance(data['image'], str):
            raise ValueError("Campo 'image' debe ser string")
        
        # Validar modo si existe
        if 'mode' in data:
            valid_modes = PromptService.get_available_modes()
            if data['mode'] not in valid_modes:
                raise ValueError(f"Modo inválido. Opciones: {', '.join(valid_modes)}")
        
        # Validar prompt personalizado si existe
        if 'custom_prompt' in data:
            if not isinstance(data['custom_prompt'], str):
                raise ValueError("Campo 'custom_prompt' debe ser string")
            if len(data['custom_prompt']) > 5000:
                raise ValueError("Prompt personalizado muy largo (máx 5000 caracteres)")
        
        return True