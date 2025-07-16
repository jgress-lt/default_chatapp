# Test Plugin - Automatic Function Calling Demo

This document explains how the TestPlugin demonstrates automatic function calling in your chat application using Semantic Kernel.

## How It Works

The TestPlugin contains three functions that can be automatically triggered by user questions:

### 1. `get_current_time()`
**Triggers when users ask about time/date:**
- "What time is it?"
- "What's the current date?"
- "When is it right now?"
- "Show me the timestamp"

**Function signature:**
```python
@kernel_function(
    name="get_current_time",
    description="Get the current date and time. Use this when users ask about the current time, date, or when something happened."
)
def get_current_time(self, format_type: str = "full") -> str:
```

### 2. `calculate_simple_math()`
**Triggers when users ask for math calculations:**
- "What's 15 + 27?"
- "Can you multiply 8 by 12?"
- "Divide 100 by 4"
- "Calculate 45 minus 13"

**Function signature:**
```python
@kernel_function(
    name="calculate_simple_math", 
    description="Perform simple mathematical calculations. Use this when users ask for basic math operations like addition, subtraction, multiplication, or division."
)
def calculate_simple_math(self, operation: str, first_number: float, second_number: float) -> str:
```

### 3. `get_plugin_stats()`
**Triggers when users ask about plugin usage:**
- "How many times have the test functions been called?"
- "Show me plugin statistics"
- "What are the test function stats?"

## Automatic Function Calling Process

When you ask a question like "What time is it?", here's what happens:

1. **AI analyzes the message** and recognizes it relates to time
2. **Semantic Kernel automatically finds** the `get_current_time` function
3. **The function is called** without any manual API calls
4. **The result is returned** as part of the AI's response

## Example Conversations

**User:** "What time is it?"
**AI:** *[Automatically calls get_current_time()]* "Current full: 2025-07-15 16:22:51"

**User:** "Can you add 25 and 17?"
**AI:** *[Automatically calls calculate_simple_math(operation="add", first_number=25, second_number=17)]* "25 add 17 = 42"

**User:** "How many times have functions been called?"
**AI:** *[Automatically calls get_plugin_stats()]* "The test plugin has been called 5 times total..."

## Key Benefits

1. **No manual API calls needed** - Functions are triggered by natural language
2. **Intelligent parameter extraction** - AI figures out what numbers to use for math
3. **Context-aware** - AI knows when to call which function
4. **Error handling** - Functions handle edge cases (like division by zero)

## Technical Implementation

The magic happens through:
- **`@kernel_function` decorator** - Makes functions available to the AI
- **Detailed descriptions** - Help the AI understand when to call functions  
- **Type annotations** - Ensure proper parameter handling
- **`FunctionChoiceBehavior.Auto()`** - Enables automatic function calling

This replaces the need for manual `/invoke` endpoints - the AI now decides when and how to call functions based on user intent!

## 📊 Enhanced Logging

The system now includes comprehensive logging to track user questions and function calls in real-time:

### User Activity Logging
```
🔵 USER QUESTION - Request ID: abc123, Content: 'What time is it?'
🤖 FUNCTION CALLING ENABLED - Auto function calling active for this request
```

### Function Call Logging
```
🟢 FUNCTION CALLED: get_current_time() - Call #1, Format: full
✅ FUNCTION RESULT: get_current_time() returned 'Current full: 2025-07-15 16:33:14'
```

### Plugin Registration Logging
```
🔌 PLUGIN REGISTERED: TestPlugin with functions: ['get_current_time', 'calculate_simple_math', 'get_plugin_stats']
✅ Default plugins registered successfully
```

### Conversation Context Logging
```
💬 CONVERSATION CONTEXT: 3 total messages in history
📊 MESSAGE BREAKDOWN: 2 user messages, 1 assistant messages
```

### Service Status Logging
```
🔥 SEMANTIC KERNEL SERVICE READY
⚡ Auto Function Calling: ENABLED
📝 Available Test Functions:
   🕐 get_current_time() - Triggers on time/date questions
   🧮 calculate_simple_math() - Triggers on math questions  
   📊 get_plugin_stats() - Triggers on plugin usage questions
```

All logs appear in the terminal when you run the server, making it easy to see what users are asking and which functions get automatically triggered!
