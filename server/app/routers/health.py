from fastapi import APIRouter
import time

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Root endpoint for basic health check"""
    return {"message": "Azure Chat API is running"}

@router.get("/health")
async def health():
    """Detailed health check endpoint"""
    return {
        "status": "OK",
        "timestamp": time.time(),
        "service": "Azure Chat API",
        "version": "1.0.0"
    }
