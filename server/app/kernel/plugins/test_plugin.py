"""
Test Plugin for Semantic Kernel

This plugin provides a simple test function that can be automatically
triggered by the AI when users ask relevant questions.
"""

import logging
import json
from datetime import datetime
from typing import Annotated
from semantic_kernel.functions import kernel_function

log = logging.getLogger("backend.app")

class TestPlugin:
    """
    A simple test plugin to demonstrate automatic function calling.
    
    This plugin shows how the AI can automatically detect user intent
    and call appropriate functions without manual API calls.
    """
    
    def __init__(self):
        """Initialize the test plugin."""
        self.call_count = 0
        self.last_called = None
        log.info("TestPlugin initialized")
    
    @kernel_function(
        name="get_current_time",
        description="Get the current date and time. Use this when users ask about the current time, date, or when something happened."
    )
    def get_current_time(
        self,
        format_type: Annotated[str, "Format type: 'full', 'date', 'time', or 'timestamp'"] = "full"
    ) -> Annotated[str, "Current time in the requested format"]:
        """
        Get the current date and time in various formats.
        
        Args:
            format_type: How to format the time ('full', 'date', 'time', 'timestamp')
            
        Returns:
            Formatted current date/time string
        """
        try:
            now = datetime.now()
            self.call_count += 1
            self.last_called = now
            
            log.info("FUNCTION CALLED: get_current_time() - Call #%d", self.call_count)
            log.info("CURRENT TIME REQUEST - Format: %s", format_type)
            
            if format_type == "date":
                result = now.strftime("%Y-%m-%d")
            elif format_type == "time":
                result = now.strftime("%H:%M:%S")
            elif format_type == "timestamp":
                result = str(int(now.timestamp()))
            else:  # full
                result = now.strftime("%Y-%m-%d %H:%M:%S")
            
            log.info("FUNCTION RESULT: get_current_time() returned '%s'", result)
            return f"Current {format_type}: {result}"
            
        except Exception as exc:
            log.error(f"Failed to get current time: {exc}")
            return f"Error getting current time: {exc}"
    
    @kernel_function(
        name="calculate_simple_math",
        description="Perform simple mathematical calculations. Use this when users ask for basic math operations like addition, subtraction, multiplication, or division."
    )
    def calculate_simple_math(
        self,
        operation: Annotated[str, "Math operation: 'add', 'subtract', 'multiply', 'divide'"],
        first_number: Annotated[float, "First number in the calculation"],
        second_number: Annotated[float, "Second number in the calculation"]
    ) -> Annotated[str, "Result of the mathematical operation"]:
        """
        Perform simple mathematical calculations.
        
        Args:
            operation: The operation to perform ('add', 'subtract', 'multiply', 'divide')
            first_number: First number
            second_number: Second number
            
        Returns:
            Calculation result as a string
        """
        try:
            self.call_count += 1
            self.last_called = datetime.now()
            
            log.info("FUNCTION CALLED: calculate_simple_math() - Call #%d, Operation: %s %s %s", 
                    self.call_count, first_number, operation, second_number)
            
            if operation == "add":
                result = first_number + second_number
            elif operation == "subtract":
                result = first_number - second_number
            elif operation == "multiply":
                result = first_number * second_number
            elif operation == "divide":
                if second_number == 0:
                    log.warning("FUNCTION ERROR: Division by zero attempted")
                    return "Error: Cannot divide by zero"
                result = first_number / second_number
            else:
                log.warning("FUNCTION ERROR: Unknown operation '%s'", operation)
                return f"Error: Unknown operation '{operation}'. Use: add, subtract, multiply, divide"
            
            response = f"{first_number} {operation} {second_number} = {result}"
            log.info("FUNCTION RESULT: calculate_simple_math() returned '%s'", response)
            return response
            
        except Exception as exc:
            log.error(f"Failed to calculate: {exc}")
            return f"Error in calculation: {exc}"
    
    @kernel_function(
        name="get_plugin_stats",
        description="Get statistics about how many times this test plugin has been used. Use this when users ask about plugin usage or test function statistics."
    )
    def get_plugin_stats(self) -> Annotated[str, "Plugin usage statistics in JSON format"]:
        """
        Get statistics about plugin usage.
        
        Returns:
            JSON string with plugin statistics
        """
        try:
            log.info("FUNCTION CALLED: get_plugin_stats() - Call #%d", self.call_count + 1)
            
            stats = {
                "total_calls": self.call_count,
                "last_called": self.last_called.isoformat() if self.last_called else None,
                "plugin_name": "TestPlugin",
                "available_functions": ["get_current_time", "calculate_simple_math", "get_plugin_stats"],
                "status": "active"
            }
            
            result = json.dumps(stats, indent=2)
            log.info("FUNCTION RESULT: get_plugin_stats() returned stats for %d total calls", self.call_count)
            return result
            
        except Exception as exc:
            log.error(f"Failed to get plugin stats: {exc}")
            return json.dumps({"error": f"Failed to get stats: {exc}"})
