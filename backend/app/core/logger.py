import logging
import sys
from datetime import datetime

def setup_logger(name='glimpse'):
    """Configura el logger de la aplicación"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()