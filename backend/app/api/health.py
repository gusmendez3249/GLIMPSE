from flask import Blueprint, jsonify
from app.core.config import Config

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        "status": "ok",
        "service": "GLIMPSE Backend",
        "version": "1.0.0",
        "gemini_configured": bool(Config.GEMINI_API_KEY)
    }), 200

@health_bp.route('/ping', methods=['GET'])
def ping():
    """Ping simple"""
    return jsonify({"message": "pong"}), 200