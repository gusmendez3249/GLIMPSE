from flask import Blueprint

def register_api_blueprints(app):
    """Registra todos los blueprints de la API"""
    
    from app.api.health import health_bp
    from app.api.analyze import analyze_bp
    
    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(analyze_bp)