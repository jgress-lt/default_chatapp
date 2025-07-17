import time
import uuid
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Simple middleware to log HTTP requests to console only"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        logger.info("RequestLoggingMiddleware initialized for console logging only")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]  # Short ID for logs
        start_time = time.time()
        
        # Log incoming request to console
        logger.info(f"[{request_id}] {request.method} {request.url.path} - Started")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log completed request to console
            logger.info(f"[{request_id}] {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"[{request_id}] {request.method} {request.url.path} - ERROR: {str(e)} - {process_time:.2f}s")
            raise
