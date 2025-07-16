import logging
import os

def setup_logging():
    """Simple console-only logging setup"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Clear any existing handlers first
    logging.getLogger().handlers.clear()
    
    # Basic console logging format
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],  # Only console handler
        force=True  # Override any existing configuration
    )
    
    # Ensure Azure SDK logs go to console only
    azure_logger = logging.getLogger("azure")
    azure_logger.handlers.clear()
    azure_logger.addHandler(logging.StreamHandler())
    azure_logger.setLevel(logging.WARNING)  # Reduce Azure SDK verbosity
