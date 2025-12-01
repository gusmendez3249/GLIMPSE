from flask import Flask, jsonify
from flask_cors import CORS
from app.core.config import Config
from app.core.logger import logger

def create_app():
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Validar configuración
    try:
        Config.validate()
        logger.info("Configuración validada correctamente")
    except ValueError as e:
        logger.error(f"Error en configuración: {str(e)}")
        raise
    
    # Registrar blueprints
    from app.api import register_api_blueprints
    register_api_blueprints(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint no encontrado"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {str(error)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Error no manejado: {str(error)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
    logger.info("Aplicación Flask inicializada")
    return app