"""
Semantic Kernel Azure OpenAI Service

This module provides Azure OpenAI integration using Semantic Kernel
following best practices for AI orchestration and error handling.

This replaces the direct OpenAI client usage with Semantic Kernel
for better abstraction and plugin support.
"""

import json
import time
import uuid
import logging
from typing import AsyncGenerator, List, Dict, Optional
from dotenv import load_dotenv

from app.kernel.services.chat_service import get_chat_service

# Load environment
load_dotenv()

# Configure logging
log = logging.getLogger("backend.app")

# Initialize the Semantic Kernel chat service
log.info("🔄 INITIALIZING SEMANTIC KERNEL CHAT SERVICE...")
chat_service = get_chat_service()

# Log startup information
log.info("🔥 SEMANTIC KERNEL SERVICE READY")
log.info("⚡ Auto Function Calling: ENABLED")
log.info("📝 Available Test Functions:")
log.info("   🕐 get_current_time() - Triggers on time/date questions")
log.info("   🧮 calculate_simple_math() - Triggers on math questions")  
log.info("   📊 get_plugin_stats() - Triggers on plugin usage questions")
log.info("💡 Example questions: 'What time is it?', 'What's 5+3?', 'Show plugin stats'")

# Force initialization to ensure plugins are loaded
log.info("🔧 FORCING KERNEL AND PLUGIN INITIALIZATION...")
if hasattr(chat_service, 'kernel') and hasattr(chat_service.kernel, 'plugins'):
    plugin_names = list(chat_service.kernel.plugins.keys()) if hasattr(chat_service.kernel.plugins, 'keys') else []
    log.info("🔌 LOADED KERNEL PLUGINS: %s", plugin_names)
    
    # Log each plugin's functions
    for plugin_name in plugin_names:
        try:
            plugin = chat_service.kernel.plugins[plugin_name]
            if hasattr(plugin, '__dict__'):
                functions = [attr for attr in dir(plugin) if not attr.startswith('_') and callable(getattr(plugin, attr))]
                log.info("   📦 %s functions: %s", plugin_name, functions[:5])  # Limit to first 5
        except Exception as e:
            log.warning("   ⚠️ Could not inspect plugin %s: %s", plugin_name, e)
else:
    log.warning("⚠️ KERNEL OR PLUGINS NOT ACCESSIBLE - Function calling may not work")

async def azure_stream(
    msgs: List[Dict[str, str]],
    max_tokens: int,
    temperature: float,
    request_id: str = None,
) -> AsyncGenerator[bytes, None]:
    """
    Generate streaming chat completions using Semantic Kernel.
    
    Args:
        msgs: List of chat messages with 'role' and 'content' keys
        max_tokens: Maximum number of tokens to generate  
        temperature: Sampling temperature (0.0 to 2.0)
        request_id: Optional request identifier for tracking
        
    Yields:
        bytes: Formatted streaming response chunks
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    
    log.info(
        "🚀 STARTING STREAMING CHAT - Request ID: %s, Messages: %d, Max tokens: %d, Temperature: %.2f",
        request_id,
        len(msgs),
        max_tokens,
        temperature
    )
    
    # Log conversation context
    if msgs:
        log.info("💬 CONVERSATION CONTEXT: %d total messages in history", len(msgs))
        user_msgs = [m for m in msgs if m.get("role") == "user"]
        assistant_msgs = [m for m in msgs if m.get("role") == "assistant"]
        log.info("📊 MESSAGE BREAKDOWN: %d user messages, %d assistant messages", 
                len(user_msgs), len(assistant_msgs))
        
        # Log the latest user message to see what the user is asking
        if user_msgs:
            latest_user_msg = user_msgs[-1].get("content", "")
            log.info("🔵 LATEST USER QUESTION: '%s'", 
                    latest_user_msg[:200] + "..." if len(latest_user_msg) > 200 else latest_user_msg)
    
    try:
        # Use Semantic Kernel chat service for streaming
        async for chunk in chat_service.stream_chat(
            messages=msgs,
            max_tokens=max_tokens,
            temperature=temperature,
            request_id=request_id,
        ):
            yield chunk
            
    except Exception as exc:
        log.error("❌ STREAMING ERROR - Request ID: %s, Error: %s", request_id, exc)
        
        # Send error response in the expected format
        error_payload = {
            "error": "Streaming failed",
            "detail": str(exc),
            "request_id": request_id
        }
        yield f"data: {json.dumps(error_payload)}\n\n".encode("utf-8")
    
    log.info("✅ STREAMING COMPLETED - Request ID: %s", request_id)

async def non_stream_chat(
    msgs: List[Dict[str, str]],
    max_tokens: int,
    temperature: float,
    request_id: str = None,
) -> Dict[str, str]:
    """
    Generate non-streaming chat completion using Semantic Kernel.
    
    Args:
        msgs: List of chat messages with 'role' and 'content' keys
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature (0.0 to 2.0)
        request_id: Optional request identifier for tracking
        
    Returns:
        Dictionary containing the response content
        
    Raises:
        Exception: If completion fails
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    
    log.info(
        "🚀 STARTING NON-STREAMING CHAT - Request ID: %s, Messages: %d, Max tokens: %d, Temperature: %.2f",
        request_id,
        len(msgs),
        max_tokens,
        temperature
    )
    
    # Log conversation context
    if msgs:
        log.info("💬 CONVERSATION CONTEXT: %d total messages in history", len(msgs))
        user_msgs = [m for m in msgs if m.get("role") == "user"]
        assistant_msgs = [m for m in msgs if m.get("role") == "assistant"]
        log.info("📊 MESSAGE BREAKDOWN: %d user messages, %d assistant messages", 
                len(user_msgs), len(assistant_msgs))
                
        # Log the latest user message to see what the user is asking
        if user_msgs:
            latest_user_msg = user_msgs[-1].get("content", "")
            log.info("🔵 LATEST USER QUESTION: '%s'", 
                    latest_user_msg[:200] + "..." if len(latest_user_msg) > 200 else latest_user_msg)
    
    try:
        # Use Semantic Kernel chat service for completion
        result = await chat_service.complete_chat(
            messages=msgs,
            max_tokens=max_tokens,
            temperature=temperature,
            request_id=request_id,
        )
        
        log.info("✅ NON-STREAMING COMPLETED - Request ID: %s", request_id)
        return result
        
    except Exception as exc:
        log.error("❌ NON-STREAMING ERROR - Request ID: %s, Error: %s", request_id, exc)
        raise exc

# Backward compatibility functions (keeping the same interface)
def azure_stream_sync(*args, **kwargs):
    """Synchronous wrapper for azure_stream (for backward compatibility)."""
    import asyncio
    
    async def _async_wrapper():
        async for chunk in azure_stream(*args, **kwargs):
            yield chunk
    
    # Note: This is a simplified sync wrapper. In production, you might want
    # to handle this differently based on your specific needs.
    return _async_wrapper()

# Additional utility functions for Semantic Kernel integration
async def get_kernel_info() -> Dict[str, str]:
    """
    Get information about the current Semantic Kernel configuration.
    
    Returns:
        Dictionary with kernel configuration details
    """
    try:
        kernel = chat_service.kernel
        services = kernel.services
        
        info = {
            "kernel_initialized": "true",
            "services_count": str(len(services)),
            "chat_service_available": "true" if chat_service.chat_service else "false",
        }
        
        # Get service details if available
        if chat_service.chat_service:
            info["service_type"] = type(chat_service.chat_service).__name__
        
        return info
        
    except Exception as exc:
        log.error("Failed to get kernel info: %s", exc)
        return {
            "kernel_initialized": "false",
            "error": str(exc)
        }

async def validate_kernel_health() -> bool:
    """
    Validate that the Semantic Kernel is healthy and ready to use.
    
    Returns:
        True if kernel is healthy, False otherwise
    """
    try:
        # Simple health check - try to create a basic chat history
        test_messages = [{"role": "user", "content": "test"}]
        chat_history = chat_service._create_chat_history(test_messages)
        return len(chat_history.messages) > 0
        
    except Exception as exc:
        log.error("Kernel health check failed: %s", exc)
        return False
