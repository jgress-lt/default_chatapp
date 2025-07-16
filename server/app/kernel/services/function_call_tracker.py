"""
Function Call Tracker for Semantic Kernel

This module provides tracking capabilities for function calls during
streaming chat conversations, allowing metadata to be sent at the end
of streaming responses.
"""

import json
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

log = logging.getLogger("backend.app")

class FunctionCallTracker:
    """Tracks function calls during a conversation for streaming responses."""
    
    def __init__(self):
        self.function_calls: List[Dict[str, Any]] = []
        self.request_id: Optional[str] = None
        self.tracking_active: bool = False
        
    def start_tracking(self, request_id: str):
        """Start tracking function calls for a request."""
        self.request_id = request_id
        self.function_calls = []
        self.tracking_active = True
        log.info("FUNCTION CALL TRACKING STARTED - Request ID: %s", request_id)
    
    def record_function_call(self, 
                           function_name: str, 
                           plugin_name: str,
                           parameters: Dict[str, Any] = None,
                           result: str = None,
                           execution_time: float = None):
        """Record a function call."""
        if not self.tracking_active:
            return
            
        call_info = {
            "function_name": function_name,
            "plugin_name": plugin_name,
            "parameters": parameters or {},
            "result": result,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "call_order": len(self.function_calls) + 1
        }
        
        self.function_calls.append(call_info)
        log.info("FUNCTION CALL RECORDED: %s.%s() - Call #%d", 
                plugin_name, function_name, len(self.function_calls))
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all function calls."""
        return {
            "request_id": self.request_id,
            "total_function_calls": len(self.function_calls),
            "function_calls": self.function_calls,
            "functions_used": list(set(f"{call['plugin_name']}.{call['function_name']}" 
                                     for call in self.function_calls)),
            "tracking_timestamp": datetime.now().isoformat()
        }
    
    def has_function_calls(self) -> bool:
        """Check if any function calls were recorded."""
        return len(self.function_calls) > 0
    
    def clear(self):
        """Clear tracked function calls."""
        self.function_calls = []
        self.request_id = None
        self.tracking_active = False
        log.debug("Function call tracking cleared")

# Global tracker instance
_tracker_instance: Optional[FunctionCallTracker] = None

def get_function_call_tracker() -> FunctionCallTracker:
    """Get the global function call tracker instance."""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = FunctionCallTracker()
    return _tracker_instance
