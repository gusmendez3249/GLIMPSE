import gc
import time
from flask import Blueprint, request, jsonify
from app.services.gemini_service import gemini_service
from app.services.image_service import ImageService
from app.core.rate_limiter import rate_limiter
from app.core.logger import logger

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Analiza una imagen capturada
    
    Body JSON:
    {
        "image": "data:image/png;base64,...",
        "mode": "detailed",  # quick, detailed, code, document, creative
        "custom_prompt": "..." # opcional
    }
    """
    
    # Rate limiting
    if not rate_limiter.is_allowed():
        return jsonify({
            "error": "Demasiadas solicitudes. Espera un momento."
        }), 429
    
    try:
        # Validar request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibió datos"}), 400
        
        if 'image' not in data:
            return jsonify({"error": "No se recibió imagen"}), 400
        
        # Extraer parámetros
        image_data = data['image']
        mode = data.get('mode', 'detailed')
        custom_prompt = data.get('custom_prompt', None)
        
        logger.info(f"Procesando análisis en modo: {mode}")
        
        # Procesar imagen
        image = ImageService.process_base64_image(image_data)
        
        # Analizar con Gemini
        response_text = gemini_service.analyze_image(
            image=image,
            mode=mode,
            custom_prompt=custom_prompt
        )
        
        # Limpiar memoria
        del image
        gc.collect()
        
        # Respuesta
        result = {
            "response": response_text,
            "mode": mode,
            "timestamp": time.time(),
            "remaining_requests": rate_limiter.get_remaining()
        }
        
        logger.info("Análisis completado exitosamente")
        return jsonify(result), 200
        
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        gc.collect()
        return jsonify({"error": str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error interno: {str(e)}")
        gc.collect()
        return jsonify({"error": "Error interno del servidor"}), 500