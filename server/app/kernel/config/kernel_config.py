"""
Semantic Kernel Configuration Module

This module handles the configuration and initialization of the Semantic Kernel
for Azure OpenAI integration following best practices.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env.local'))

# Configure logging
log = logging.getLogger("semantic_kernel")

class SemanticKernelConfig:
    """Configuration class for Semantic Kernel Azure OpenAI integration."""
    
    def __init__(self):
        """Initialize the Semantic Kernel configuration."""
        # Azure OpenAI configuration from environment variables
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
        
        # Validate required configuration
        self._validate_config()
        
        log.info("=== Semantic Kernel Azure OpenAI Configuration ===")
        log.info("Endpoint      : %s", self.endpoint)
        log.info("Deployment    : %s", self.deployment_name)
        log.info("API version   : %s", self.api_version)
        log.info("API key       : %s", f"{self.api_key[:8]}..." if self.api_key else "NOT SET")
        log.info("================================================")
    
    def _validate_config(self) -> None:
        """Validate that all required configuration is present."""
        if not all([self.endpoint, self.api_key, self.deployment_name]):
            raise RuntimeError(
                "Missing Azure OpenAI configuration for Semantic Kernel. "
                "Ensure AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT are set."
            )

class KernelFactory:
    """Factory class for creating and configuring Semantic Kernel instances."""
    
    @staticmethod
    def create_kernel(config: Optional[SemanticKernelConfig] = None) -> Kernel:
        """
        Create and configure a Semantic Kernel instance with Azure OpenAI.
        
        Args:
            config: Optional SemanticKernelConfig instance. If None, creates a new one.
            
        Returns:
            Configured Kernel instance with Azure OpenAI chat completion service.
            
        Raises:
            RuntimeError: If configuration is invalid or service creation fails.
        """
        if config is None:
            config = SemanticKernelConfig()
        
        try:
            # Create the kernel
            kernel = Kernel()
            
            # Configure Azure OpenAI chat completion service
            chat_service = AzureChatCompletion(
                service_id="azure_openai_chat",
                deployment_name=config.deployment_name,
                endpoint=config.endpoint,
                api_key=config.api_key,
                api_version=config.api_version,
            )
            
            # Add the service to the kernel
            kernel.add_service(chat_service)
            
            log.info("Semantic Kernel initialized successfully with Azure OpenAI")
            return kernel
            
        except Exception as exc:
            log.error("Failed to initialize Semantic Kernel: %s", exc)
            raise RuntimeError(f"Semantic Kernel initialization failed: {exc}") from exc
    
    @staticmethod
    def get_chat_service(kernel: Kernel) -> ChatCompletionClientBase:
        """
        Get the chat completion service from the kernel.
        
        Args:
            kernel: The configured Kernel instance.
            
        Returns:
            The chat completion service.
            
        Raises:
            RuntimeError: If no chat service is found.
        """
        try:
            chat_service = kernel.get_service(type=ChatCompletionClientBase)
            return chat_service
        except Exception as exc:
            log.error("Failed to get chat service from kernel: %s", exc)
            raise RuntimeError(f"Chat service not found in kernel: {exc}") from exc

# Global kernel instance (singleton pattern for this application)
_kernel_instance: Optional[Kernel] = None

def get_kernel() -> Kernel:
    """
    Get or create the global Semantic Kernel instance.
    
    Returns:
        The global Kernel instance.
    """
    global _kernel_instance
    
    if _kernel_instance is None:
        config = SemanticKernelConfig()
        _kernel_instance = KernelFactory.create_kernel(config)
    
    return _kernel_instance

def reset_kernel() -> None:
    """Reset the global kernel instance (useful for testing)."""
    global _kernel_instance
    _kernel_instance = None
