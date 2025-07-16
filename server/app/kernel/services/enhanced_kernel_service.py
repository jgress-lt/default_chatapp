"""
Enhanced Semantic Kernel Service with Plugin Management

This service extends the basic kernel configuration to include
plugin management and advanced capabilities.
"""

import logging
from typing import Optional, Dict, Any, List
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelPlugin

from app.kernel.config.kernel_config import get_kernel
from app.kernel.plugins.test_plugin import TestPlugin

log = logging.getLogger("backend.app")

class EnhancedKernelService:
    """
    Enhanced Semantic Kernel service with plugin management capabilities.
    
    This service provides:
    - Plugin registration and management
    - Function calling capabilities
    - Kernel health monitoring
    - Advanced configuration options
    """
    
    def __init__(self, kernel: Optional[Kernel] = None):
        """
        Initialize the enhanced kernel service.
        
        Args:
            kernel: Optional pre-configured Kernel instance
        """
        self.kernel = kernel or get_kernel()
        self.plugins: Dict[str, Any] = {}
        
        # Initialize and register default plugins
        self._register_default_plugins()
        
        log.info("Enhanced Kernel Service initialized with %d plugins", len(self.plugins))
        log.info("Available plugins: %s", list(self.plugins.keys()))
    
    def _register_default_plugins(self) -> None:
        """Register the default plugins with the kernel."""
        try:
            # Register Test Plugin for automatic function calling demonstrations
            test_plugin = TestPlugin()
            self.kernel.add_plugin(test_plugin, plugin_name="TestPlugin")
            self.plugins["TestPlugin"] = test_plugin
            
            log.info("PLUGIN REGISTERED: TestPlugin with functions: %s", 
                    ["get_current_time", "calculate_simple_math", "get_plugin_stats"])
            log.info("Default plugins registered successfully")
            
        except Exception as exc:
            log.error("Failed to register default plugins: %s", exc)
            raise
    
    def add_plugin(self, plugin: Any, plugin_name: str) -> bool:
        """
        Add a custom plugin to the kernel.
        
        Args:
            plugin: The plugin instance to add
            plugin_name: Name for the plugin
            
        Returns:
            True if plugin was added successfully, False otherwise
        """
        try:
            self.kernel.add_plugin(plugin, plugin_name=plugin_name)
            self.plugins[plugin_name] = plugin
            
            log.info("Plugin '%s' added successfully", plugin_name)
            return True
            
        except Exception as exc:
            log.error("Failed to add plugin '%s': %s", plugin_name, exc)
            return False
    
    async def validate_health(self) -> bool:
        """
        Perform a comprehensive health check of the kernel and plugins.
        
        Returns:
            True if all components are healthy, False otherwise
        """
        try:
            # Check kernel basic functionality
            if not self.kernel:
                return False
            
            # Check services
            if not self.kernel.services:
                return False
            
            # Test plugin functionality with a simple function call
            try:
                chat_utils = self.plugins.get("ChatUtilities")
                if chat_utils:
                    test_result = chat_utils.validate_message("test message")
                    if "true" not in test_result.lower():
                        log.warning("Plugin health check failed")
                        return False
            except Exception as plugin_exc:
                log.warning("Plugin health check failed: %s", plugin_exc)
                # Don't fail the entire health check for plugin issues
            
            log.info("Kernel health check passed")
            return True
            
        except Exception as exc:
            log.error("Kernel health check failed: %s", exc)
            return False

# Global enhanced service instance
_enhanced_service: Optional[EnhancedKernelService] = None

def get_enhanced_kernel_service() -> EnhancedKernelService:
    """
    Get or create the global enhanced kernel service instance.
    
    Returns:
        The global EnhancedKernelService instance
    """
    global _enhanced_service
    
    if _enhanced_service is None:
        _enhanced_service = EnhancedKernelService()
    
    return _enhanced_service
