"""
Semantic Kernel Management Router

This router provides endpoints for managing Semantic Kernel plugins
and demonstrating advanced AI orchestration capabilities.
"""

import json
import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

from app.kernel.services.enhanced_kernel_service import get_enhanced_kernel_service

# Configure logging
log = logging.getLogger("kernel_router")

router = APIRouter(prefix="/api/kernel", tags=["semantic-kernel"])

@router.get("/status")
async def get_kernel_status():
    """
    Get basic status of the Semantic Kernel.
    
    Returns:
        Basic kernel health and plugin information
    """
    try:
        enhanced_service = get_enhanced_kernel_service()
        is_healthy = await enhanced_service.validate_health()
        
        return JSONResponse({
            "kernel_initialized": True,
            "healthy": is_healthy,
            "plugins_count": len(enhanced_service.plugins),
            "services_available": len(enhanced_service.kernel.services) > 0
        })
        
    except Exception as exc:
        log.error("Failed to get kernel status: %s", exc)
        raise HTTPException(status_code=500, detail=f"Failed to get kernel status: {exc}")
