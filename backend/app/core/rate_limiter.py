import time
from app.core.config import Config

class RateLimiter:
    """Control de tasa de peticiones"""
    
    def __init__(self):
        self.requests = {}
        self.window_size = 60  # segundos
        self.max_requests = Config.MAX_REQUESTS_PER_MINUTE
    
    def is_allowed(self, client_id='default'):
        """Verifica si el cliente puede hacer una petición"""
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Limpiar peticiones antiguas
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < self.window_size
        ]
        
        # Verificar límite
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Registrar nueva petición
        self.requests[client_id].append(current_time)
        return True
    
    def get_remaining(self, client_id='default'):
        """Obtiene el número de peticiones restantes"""
        if client_id not in self.requests:
            return self.max_requests
        return self.max_requests - len(self.requests[client_id])

# Instancia global
rate_limiter = RateLimiter()