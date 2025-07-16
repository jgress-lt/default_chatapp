import time
import uuid
import logging
from typing import Callable
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Simple middleware to log requests to console and Cosmos DB"""
    
    def __init__(self, app: ASGIApp, cosmos_container=None):
        super().__init__(app)
        self.cosmos_container = cosmos_container
        logger.info(f"RequestLoggingMiddleware initialized with cosmos_container: {cosmos_container is not None}")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]  # Short ID for logs
        start_time = time.time()
        
        # Log incoming request to console
        logger.info(f"[{request_id}] {request.method} {request.url.path} - Started")
        
        # Log to Cosmos DB if available
        if self.cosmos_container:
            await self._log_inbound_request(request, request_id)
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log completed request to console
            logger.info(f"[{request_id}] {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
            
            # Log to Cosmos DB if available
            if self.cosmos_container:
                await self._log_outbound_response(request, response, request_id, process_time)
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"[{request_id}] {request.method} {request.url.path} - ERROR: {str(e)} - {process_time:.2f}s")
            
            # Log error to Cosmos DB if available
            if self.cosmos_container:
                await self._log_error_response(request, request_id, process_time, str(e))
            
            raise
    
    async def _log_inbound_request(self, request: Request, request_id: str):
        """Log inbound request to Cosmos DB"""
        try:
            logger.info(f"[{request_id}] Attempting to log inbound request to Cosmos DB")
            logger.debug(f"[{request_id}] Container: {self.cosmos_container}")
            
            inbound_doc = {
                "id": f"inbound_{request_id}",
                "type": "inbound_request",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "headers": {k: v for k, v in request.headers.items() 
                           if k.lower() not in ['authorization', 'cookie']},
                "client_host": getattr(request.client, 'host', None) if request.client else None,
                "sessionId": request_id
            }
            
            logger.debug(f"[{request_id}] Document to create: {inbound_doc}")
            result = self.cosmos_container.create_item(body=inbound_doc)
            logger.info(f"[{request_id}] Successfully logged inbound request to Cosmos DB. Result: {result}")
            
        except Exception as e:
            logger.error(f"[{request_id}] Failed to log inbound request to Cosmos: {e}", exc_info=True)
    
    async def _log_outbound_response(self, request: Request, response: Response, request_id: str, process_time: float):
        """Log outbound response to Cosmos DB"""
        try:
            logger.info(f"[{request_id}] Attempting to log outbound response to Cosmos DB")
            
            outbound_doc = {
                "id": f"outbound_{request_id}",
                "type": "outbound_response",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "processing_time_ms": round(process_time * 1000, 2),
                "sessionId": request_id
            }
            
            logger.debug(f"[{request_id}] Outbound document to create: {outbound_doc}")
            result = self.cosmos_container.create_item(body=outbound_doc)
            logger.info(f"[{request_id}] Successfully logged outbound response to Cosmos DB. Result: {result}")
            
        except Exception as e:
            logger.error(f"[{request_id}] Failed to log outbound response to Cosmos: {e}", exc_info=True)
    
    async def _log_error_response(self, request: Request, request_id: str, process_time: float, error: str):
        """Log error response to Cosmos DB"""
        try:
            logger.info(f"[{request_id}] Attempting to log error to Cosmos DB")
            
            error_doc = {
                "id": f"error_{request_id}",
                "type": "error_response",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "error": error,
                "processing_time_ms": round(process_time * 1000, 2),
                "sessionId": request_id  # Partition key
            }
            
            self.cosmos_container.create_item(body=error_doc)
            logger.info(f"[{request_id}] Successfully logged error to Cosmos DB")
            
        except Exception as e:
            logger.error(f"[{request_id}] Failed to log error to Cosmos: {e}")
