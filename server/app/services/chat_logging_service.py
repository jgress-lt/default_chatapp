"""
Chat Logging Service

This module provides comprehensive logging of chat conversations to Cosmos DB,
including user questions and AI responses for both streaming and non-streaming requests.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from azure.cosmos.container import ContainerProxy

log = logging.getLogger("backend.app")

class ChatLoggingService:
    """
    Service for logging chat conversations to Cosmos DB.
    
    This service captures user questions and AI responses, providing
    comprehensive conversation tracking for analytics and debugging.
    """
    
    def __init__(self, cosmos_container: Optional[ContainerProxy] = None):
        """
        Initialize the chat logging service.
        
        Args:
            cosmos_container: Cosmos DB container for storing chat logs
        """
        self.cosmos_container = cosmos_container
        if cosmos_container:
            log.info("Chat Logging Service initialized with Cosmos DB container")
        else:
            log.warning("Chat Logging Service initialized WITHOUT Cosmos DB container - logging disabled")
    
    async def log_chat_request(
        self,
        request_id: str,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float,
        is_streaming: bool = True
    ) -> None:
        """
        Log the incoming chat request with user question.
        
        Args:
            request_id: Unique identifier for the request
            messages: List of chat messages
            max_tokens: Maximum tokens requested
            temperature: Temperature setting
            is_streaming: Whether this is a streaming request
        """
        if not self.cosmos_container:
            log.debug("Cosmos DB container not available - skipping chat request logging")
            return
        
        try:
            # Extract user question (latest user message)
            user_question = ""
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            if user_messages:
                user_question = user_messages[-1].get("content", "")
            
            # Create chat request document
            request_doc = {
                "id": f"chat_request_{request_id}",
                "type": "chat_request",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "user_question": user_question,
                "full_conversation": messages,
                "conversation_length": len(messages),
                "user_message_count": len(user_messages),
                "assistant_message_count": len([msg for msg in messages if msg.get("role") == "assistant"]),
                "request_settings": {
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "is_streaming": is_streaming
                },
                "sessionId": request_id  # Partition key
            }
            
            # Save to Cosmos DB
            result = self.cosmos_container.create_item(body=request_doc)
            log.info(
                "CHAT REQUEST LOGGED TO COSMOS - Request ID: %s, User Question: '%s'",
                request_id,
                user_question[:100] + "..." if len(user_question) > 100 else user_question
            )
            
        except Exception as e:
            log.error(
                "Failed to log chat request to Cosmos DB - Request ID: %s, Error: %s",
                request_id,
                e,
                exc_info=True
            )
    
    async def log_chat_response(
        self,
        request_id: str,
        response_content: str,
        processing_time: float,
        chunk_count: Optional[int] = None,
        function_calls: Optional[List[Dict]] = None,
        is_streaming: bool = True
    ) -> None:
        """
        Log the AI response after completion.
        
        Args:
            request_id: Unique identifier for the request
            response_content: Complete AI response content
            processing_time: Time taken to process the request
            chunk_count: Number of chunks for streaming (if applicable)
            function_calls: List of function calls made during processing
            is_streaming: Whether this was a streaming response
        """
        if not self.cosmos_container:
            log.debug("Cosmos DB container not available - skipping chat response logging")
            return
        
        try:
            # Create chat response document
            response_doc = {
                "id": f"chat_response_{request_id}",
                "type": "chat_response",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "response_content": response_content,
                "response_length": len(response_content),
                "processing_time_seconds": round(processing_time, 3),
                "performance_metrics": {
                    "chunk_count": chunk_count,
                    "is_streaming": is_streaming,
                    "processing_time_seconds": round(processing_time, 3)
                },
                "function_calls": function_calls or [],
                "function_call_count": len(function_calls) if function_calls else 0,
                "sessionId": request_id  # Partition key
            }
            
            # Save to Cosmos DB
            result = self.cosmos_container.create_item(body=response_doc)
            log.info(
                "CHAT RESPONSE LOGGED TO COSMOS - Request ID: %s, Response Length: %d chars, Processing Time: %.2fs",
                request_id,
                len(response_content),
                processing_time
            )
            
            if function_calls:
                log.info(
                    "FUNCTION CALLS LOGGED TO COSMOS - Request ID: %s, Function Count: %d",
                    request_id,
                    len(function_calls)
                )
            
        except Exception as e:
            log.error(
                "Failed to log chat response to Cosmos DB - Request ID: %s, Error: %s",
                request_id,
                e,
                exc_info=True
            )
    
    async def log_chat_conversation(
        self,
        request_id: str,
        user_question: str,
        ai_response: str,
        processing_time: float,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Log a complete conversation turn (question + response) in a single document.
        
        Args:
            request_id: Unique identifier for the request
            user_question: The user's question
            ai_response: The AI's response
            processing_time: Time taken to process
            metadata: Additional metadata (function calls, settings, etc.)
        """
        if not self.cosmos_container:
            log.debug("Cosmos DB container not available - skipping conversation logging")
            return
        
        try:
            # Create conversation document
            conversation_doc = {
                "id": f"conversation_{request_id}",
                "type": "conversation_turn",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "user_question": user_question,
                "ai_response": ai_response,
                "question_length": len(user_question),
                "response_length": len(ai_response),
                "processing_time_seconds": round(processing_time, 3),
                "metadata": metadata or {},
                "sessionId": request_id  # Partition key
            }
            
            # Save to Cosmos DB
            result = self.cosmos_container.create_item(body=conversation_doc)
            log.info(
                "CONVERSATION LOGGED TO COSMOS - Request ID: %s, Q: %d chars, A: %d chars",
                request_id,
                len(user_question),
                len(ai_response)
            )
            
        except Exception as e:
            log.error(
                "Failed to log conversation to Cosmos DB - Request ID: %s, Error: %s",
                request_id,
                e,
                exc_info=True
            )

# Global service instance (singleton pattern)
_chat_logging_service: Optional[ChatLoggingService] = None

def get_chat_logging_service() -> ChatLoggingService:
    """
    Get or create the global chat logging service instance.
    
    Returns:
        The global ChatLoggingService instance.
    """
    global _chat_logging_service
    
    if _chat_logging_service is None:
        # Import here to avoid circular imports
        try:
            from app import request_logs_container
            _chat_logging_service = ChatLoggingService(request_logs_container)
        except ImportError:
            log.warning("Could not import Cosmos DB container - chat logging will be disabled")
            _chat_logging_service = ChatLoggingService(None)
    
    return _chat_logging_service
