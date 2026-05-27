from app import create_app
from app.core.config import Config
from app.core.logger import logger
from waitress import serve

def main():
    """Punto de entrada de la aplicación"""

    # Banner
    print("=" * 60)
    print("  GLIMPSE Backend Server")
    print("=" * 60)
    print(f"  URL: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print(f"  AI Provider: {Config.PRIMARY_AI_PROVIDER.upper()}")
    print(f"  Claude API: {'OK' if Config.CLAUDE_API_KEY else 'MISSING'}")
    print(f"  Entorno: {Config.FLASK_ENV}")
    print("=" * 60)
    print()
    
    # Crear app
    app = create_app()
    
    # Iniciar servidor
    try:
        if Config.FLASK_ENV == 'development':
            logger.info("Iniciando servidor en modo desarrollo...")
            app.run(
                host=Config.FLASK_HOST,
                port=Config.FLASK_PORT,
                debug=False,
                threaded=True
            )
        else:
            logger.info("Iniciando servidor en modo producción con Waitress...")
            serve(
                app,
                host=Config.FLASK_HOST,
                port=Config.FLASK_PORT,
                threads=4
            )
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error al iniciar servidor: {str(e)}")
        raise

if __name__ == '__main__':
    main()