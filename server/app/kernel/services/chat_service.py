"""
Semantic Kernel Chat Service

This module provides chat completion services using Semantic Kernel
for Azure OpenAI integration with proper error handling and streaming support.
"""

import json
import time
import uuid
import logging
from typing import Generator, List, Dict, Optional, AsyncGenerator
from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory, ChatMessageContent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from app.kernel.config.kernel_config import get_kernel, KernelFactory
from app.kernel.services.enhanced_kernel_service import get_enhanced_kernel_service

# Configure logging
log = logging.getLogger("backend.app")

# Import chat logging service for Cosmos DB logging
try:
    from app.services.chat_logging_service import get_chat_logging_service
    CHAT_LOGGING_AVAILABLE = True
except ImportError:
    log.warning("Chat logging service not available - Cosmos DB chat logging disabled")
    CHAT_LOGGING_AVAILABLE = False

class SemanticKernelChatService:
    """
    Chat service using Semantic Kernel for Azure OpenAI integration.
    
    This service provides both streaming and non-streaming chat completion
    with proper error handling, retry logic, and performance monitoring.
    """
    
    def __init__(self, kernel: Optional[Kernel] = None):
        """
        Initialize the Semantic Kernel chat service.
        
        Args:
            kernel: Optional pre-configured Kernel instance. If None, uses enhanced kernel with plugins.
        """
        if kernel is None:
            # Use the enhanced kernel service that has plugins registered
            enhanced_service = get_enhanced_kernel_service()
            self.kernel = enhanced_service.kernel
        else:
            self.kernel = kernel
            
        self.chat_service = KernelFactory.get_chat_service(self.kernel)
        
        log.info("Semantic Kernel Chat Service initialized with automatic function calling")
        log.info("Function calling behavior: Auto() - AI will automatically detect and call functions")
        
        # Log available plugins
        try:
            plugin_names = list(self.kernel.plugins.keys()) if hasattr(self.kernel.plugins, 'keys') else []
            if plugin_names:
                log.info("Loaded plugins: %s", plugin_names)
            else:
                log.warning("No plugins loaded - function calling may not work")
        except Exception as e:
            log.warning("Could not check plugins: %s", e)
    
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        request_id: Optional[str] = None,
    ) -> AsyncGenerator[bytes, None]:
        """
        Generate streaming chat completions using Semantic Kernel.
        
        Args:
            messages: List of chat messages with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 2.0)
            request_id: Optional request identifier for tracking
            
        Yields:
            bytes: Formatted streaming response chunks
            
        Raises:
            Exception: If streaming fails
        """
        if request_id is None:
            request_id = str(uuid.uuid4())
        
        start_time = time.time()
        chunk_count = 0
        
        # Initialize chat logging service for Cosmos DB logging
        chat_logger = None
        if CHAT_LOGGING_AVAILABLE:
            try:
                chat_logger = get_chat_logging_service()
                # Log the incoming request with user question
                await chat_logger.log_chat_request(
                    request_id=request_id,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    is_streaming=True
                )
            except Exception as e:
                log.warning("Failed to initialize chat logging for Cosmos DB: %s", e)
        
        # Initialize function call tracking
        try:
            from app.kernel.services.function_call_tracker import get_function_call_tracker
            tracker = get_function_call_tracker()
            tracker.start_tracking(request_id)
        except Exception as e:
            log.warning("Failed to initialize function call tracking: %s", e)
            tracker = None
        
        try:
            # Log user questions for monitoring
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            if user_messages:
                latest_user_msg = user_messages[-1].get("content", "")
                log.info(
                    "USER QUESTION (STREAMING) - Request ID: %s, Content: '%s'",
                    request_id,
                    latest_user_msg[:200] + "..." if len(latest_user_msg) > 200 else latest_user_msg
                )
            
            # Convert messages to ChatHistory
            chat_history = self._create_chat_history(messages)
            
            # Configure execution settings with function calling enabled
            execution_settings = OpenAIPromptExecutionSettings(
                service_id="azure_openai_chat",
                max_tokens=max_tokens,
                temperature=temperature,
                function_choice_behavior=FunctionChoiceBehavior.Auto(),
            )
            
            log.info("FUNCTION CALLING ENABLED - Auto function calling active for streaming request")
            
            # Get streaming response
            stream = self.chat_service.get_streaming_chat_message_contents(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=self.kernel,
            )
            
            # Track full response for logging
            full_response_content = ""
            
            async for chunk_list in stream:
                chunk_count += 1
                
                # Handle the chunk (Semantic Kernel returns a list)
                if not chunk_list:
                    continue
                
                chunk = chunk_list[0]  # Get the first (and usually only) chunk
                
                if chunk.content:
                    # Accumulate full response content for logging
                    full_response_content += chunk.content
                    
                    # Format response to match OpenAI streaming format
                    payload = {
                        "choices": [
                            {
                                "delta": {
                                    "content": chunk.content,
                                    "role": "assistant",
                                },
                                "finish_reason": None,
                            }
                        ]
                    }
                    yield f"data: {json.dumps(payload)}\n\n".encode("utf-8")
            
            # Send function call metadata if any functions were called
            if tracker and tracker.has_function_calls():
                function_summary = tracker.get_summary()
                metadata_payload = {
                    "choices": [
                        {
                            "delta": {
                                "function_calls_metadata": function_summary
                            },
                            "finish_reason": None,
                        }
                    ]
                }
                yield f"data: {json.dumps(metadata_payload)}\n\n".encode("utf-8")
                
                log.info("FUNCTION CALL METADATA SENT - Request ID: %s, Functions called: %d", 
                        request_id, len(tracker.function_calls))
            
            # Send completion signal
            completion_payload = {
                "choices": [
                    {
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ]
            }
            yield f"data: {json.dumps(completion_payload)}\n\n".encode("utf-8")
            yield b"data: [DONE]\n\n"
            
            processing_time = time.time() - start_time
            
            # Log the full response content to console
            log.info(
                "FULL STREAMING RESPONSE - Request ID: %s, Content: '%s'",
                request_id,
                full_response_content[:1000] + "..." if len(full_response_content) > 1000 else full_response_content
            )
            print(f"\n=== STREAMING RESPONSE COMPLETE ===")
            print(f"Request ID: {request_id}")
            print(f"Full Response: {full_response_content}")
            print(f"Response Length: {len(full_response_content)} characters")
            print(f"Processing Time: {processing_time:.2f}s")
            print(f"Chunks Processed: {chunk_count}")
            print("=" * 50)
            
            # Log the complete response to Cosmos DB
            if chat_logger:
                try:
                    # Get function call summary if available
                    function_calls_summary = None
                    if tracker and tracker.has_function_calls():
                        function_calls_summary = tracker.get_summary()
                    
                    await chat_logger.log_chat_response(
                        request_id=request_id,
                        response_content=full_response_content,
                        processing_time=processing_time,
                        chunk_count=chunk_count,
                        function_calls=function_calls_summary,
                        is_streaming=True
                    )
                except Exception as e:
                    log.error("Failed to log chat response to Cosmos DB: %s", e)
            
            log.info(
                "Streaming completed - Request ID: %s, Chunks: %d, Time: %.2fs",
                request_id,
                chunk_count,
                processing_time
            )
            
        except Exception as exc:
            processing_time = time.time() - start_time
            log.error(
                "Streaming error - Request ID: %s, Time: %.2fs, Error: %s",
                request_id,
                processing_time,
                exc
            )
            
            # Send error response
            error_payload = {
                "error": "Streaming failed",
                "detail": str(exc),
                "request_id": request_id
            }
            yield f"data: {json.dumps(error_payload)}\n\n".encode("utf-8")
        finally:
            # Clear tracking data
            if tracker:
                tracker.clear()
    
    async def complete_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        request_id: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generate non-streaming chat completion using Semantic Kernel.
        
        Args:
            messages: List of chat messages with 'role' and 'content' keys
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
        
        start_time = time.time()
        
        # Initialize chat logging service for Cosmos DB logging
        chat_logger = None
        if CHAT_LOGGING_AVAILABLE:
            try:
                chat_logger = get_chat_logging_service()
                # Log the incoming request with user question
                await chat_logger.log_chat_request(
                    request_id=request_id,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    is_streaming=False
                )
            except Exception as e:
                log.warning("Failed to initialize chat logging for Cosmos DB: %s", e)
        
        try:
            # Log user questions for monitoring
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            if user_messages:
                latest_user_msg = user_messages[-1].get("content", "")
                log.info(
                    "USER QUESTION (NON-STREAMING) - Request ID: %s, Content: '%s'",
                    request_id,
                    latest_user_msg[:200] + "..." if len(latest_user_msg) > 200 else latest_user_msg
                )
            
            # Convert messages to ChatHistory
            chat_history = self._create_chat_history(messages)
            
            # Configure execution settings with function calling enabled
            execution_settings = OpenAIPromptExecutionSettings(
                service_id="azure_openai_chat",
                max_tokens=max_tokens,
                temperature=temperature,
                function_choice_behavior=FunctionChoiceBehavior.Auto(),
            )
            
            log.info("FUNCTION CALLING ENABLED - Auto function calling active for non-streaming request")
            
            # Get completion response
            response = await self.chat_service.get_chat_message_contents(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=self.kernel,
            )
            
            # Extract content from response
            if response and len(response) > 0:
                content = response[0].content
            else:
                content = ""
            
            processing_time = time.time() - start_time
            
            # Log the full response content to console
            log.info(
                "FULL NON-STREAMING RESPONSE - Request ID: %s, Content: '%s'",
                request_id,
                content[:1000] + "..." if len(content) > 1000 else content
            )
            print(f"\n=== NON-STREAMING RESPONSE COMPLETE ===")
            print(f"Request ID: {request_id}")
            print(f"Full Response: {content}")
            print(f"Response Length: {len(content)} characters")
            print(f"Processing Time: {processing_time:.2f}s")
            print("=" * 50)
            
            # Log the complete response to Cosmos DB
            if chat_logger:
                try:
                    await chat_logger.log_chat_response(
                        request_id=request_id,
                        response_content=content,
                        processing_time=processing_time,
                        chunk_count=None,  # Not applicable for non-streaming
                        function_calls=None,  # TODO: Add function call tracking for non-streaming
                        is_streaming=False
                    )
                except Exception as e:
                    log.error("Failed to log chat response to Cosmos DB: %s", e)
            
            log.info(
                "Completion successful - Request ID: %s, Time: %.2fs, Response length: %d",
                request_id,
                processing_time,
                len(content)
            )
            
            return {"response": content}
            
        except Exception as exc:
            processing_time = time.time() - start_time
            log.error(
                "Completion error - Request ID: %s, Time: %.2fs, Error: %s",
                request_id,
                processing_time,
                exc
            )
            raise exc
    
    def _create_chat_history(self, messages: List[Dict[str, str]]) -> ChatHistory:
        """
        Convert message list to Semantic Kernel ChatHistory format.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            ChatHistory object for Semantic Kernel
        """
        chat_history = ChatHistory()
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                chat_history.add_system_message(content)
            elif role == "assistant":
                chat_history.add_assistant_message(content)
            else:  # Default to user
                chat_history.add_user_message(content)
        
        return chat_history

# Global service instance (singleton pattern)
_service_instance: Optional[SemanticKernelChatService] = None

def get_chat_service() -> SemanticKernelChatService:
    """
    Get or create the global Semantic Kernel chat service instance.
    
    Returns:
        The global SemanticKernelChatService instance.
    """
    global _service_instance
    
    if _service_instance is None:
        _service_instance = SemanticKernelChatService()
    
    return _service_instance
