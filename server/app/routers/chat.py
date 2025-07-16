from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
from pydantic import BaseModel
from app.services.semantic_kernel_service import azure_stream, non_stream_chat, get_kernel_info, validate_kernel_health
import time

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = True
    max_tokens: int = 1000
    temperature: float = 0.7

@router.post("")
async def chat(request: ChatRequest, req: Request):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages array is required")

    msgs = [m.model_dump() for m in request.messages]
    
    # Get request ID from middleware (if available)
    request_id = req.headers.get("X-Request-ID")

    if request.stream:
        generator = azure_stream(
            msgs, 
            max_tokens=request.max_tokens, 
            temperature=request.temperature,
            request_id=request_id
        )
        return StreamingResponse(
            generator,
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )

    try:
        result = await non_stream_chat(
            msgs, 
            max_tokens=request.max_tokens, 
            temperature=request.temperature,
            request_id=request_id
        )
        return JSONResponse(result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/health")
async def health_check():
    """Check the health status of the Semantic Kernel service."""
    try:
        is_healthy = await validate_kernel_health()
        kernel_info = await get_kernel_info()
        
        return JSONResponse({
            "status": "healthy" if is_healthy else "unhealthy",
            "kernel_info": kernel_info,
            "timestamp": time.time()
        })
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(exc),
                "timestamp": time.time()
            }
        )

@router.get("/kernel-info")
async def kernel_info():
    """Get detailed information about the Semantic Kernel configuration."""
    try:
        info = await get_kernel_info()
        return JSONResponse(info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
