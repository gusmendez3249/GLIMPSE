import base64
from io import BytesIO
from PIL import Image
from app.core.config import Config
from app.core.logger import logger

class ImageService:
    """Servicio para procesamiento de imágenes"""
    
    @staticmethod
    def process_base64_image(image_data):
        """Procesa una imagen en base64 y retorna objeto PIL Image"""
        try:
            # Remover prefijo data:image si existe
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decodificar base64
            image_bytes = base64.b64decode(image_data)
            
            # Abrir imagen
            image = Image.open(BytesIO(image_bytes))
            
            # Optimizar tamaño si es necesario
            if image.size[0] > Config.MAX_IMAGE_SIZE[0] or image.size[1] > Config.MAX_IMAGE_SIZE[1]:
                logger.info(f"Redimensionando imagen de {image.size} a {Config.MAX_IMAGE_SIZE}")
                image.thumbnail(Config.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.error(f"Error procesando imagen: {str(e)}")
            raise ValueError(f"Error al procesar imagen: {str(e)}")
    
    @staticmethod
    def validate_image_size(image_bytes):
        """Valida que el tamaño de la imagen no exceda el límite"""
        size_mb = len(image_bytes) / (1024 * 1024)
        if size_mb > Config.MAX_FILE_SIZE_MB:
            raise ValueError(f"Imagen muy grande: {size_mb:.2f}MB (máximo {Config.MAX_FILE_SIZE_MB}MB)")
        return True