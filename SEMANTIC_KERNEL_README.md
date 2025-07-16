# Semantic Kernel Integration

This document describes the Semantic Kernel integration in the chat application, following Microsoft's best practices for AI orchestration.

## Architecture Overview

The application now uses Semantic Kernel as the AI orchestration layer, providing:

- **Plugin-based Architecture**: Extensible functionality through plugins
- **Service Abstraction**: Clean separation between AI services and business logic
- **Advanced Monitoring**: Comprehensive tracking and analytics
- **Error Handling**: Robust error handling with retry logic
- **Type Safety**: Full TypeScript-style annotations and validation

## Folder Structure

Following Semantic Kernel conventions, the code is organized as:

```
server/app/kernel/
├── __init__.py                          # Main kernel module
├── config/
│   ├── __init__.py
│   └── kernel_config.py                 # Kernel configuration and factory
├── services/
│   ├── __init__.py
│   ├── chat_service.py                  # Core chat completion service
│   └── enhanced_kernel_service.py       # Enhanced service with plugin management
└── plugins/
    ├── __init__.py
    ├── chat_utilities.py                # Chat utility functions
    └── conversation_plugin.py           # Conversation tracking and analytics
```

## Key Components

### 1. Kernel Configuration (`kernel_config.py`)

- **SemanticKernelConfig**: Manages Azure OpenAI configuration
- **KernelFactory**: Creates and configures kernel instances
- **Global Instance Management**: Singleton pattern for kernel instances

### 2. Chat Service (`chat_service.py`)

- **SemanticKernelChatService**: Core chat completion functionality
- **Streaming Support**: Async generators for real-time responses
- **Error Handling**: Comprehensive error handling and logging
- **Message Conversion**: Seamless conversion between formats

### 3. Enhanced Kernel Service (`enhanced_kernel_service.py`)

- **Plugin Management**: Dynamic plugin registration and management
- **Function Calling**: Invoke plugin functions with type safety
- **Health Monitoring**: Comprehensive kernel health checks
- **Status Reporting**: Detailed kernel and service status

### 4. Plugins

#### Chat Utilities Plugin (`chat_utilities.py`)
- `count_tokens`: Estimate token count for text
- `format_response`: Format responses with markdown/HTML
- `validate_message`: Validate message content and length

#### Conversation Plugin (`conversation_plugin.py`)
- `add_conversation_message`: Track conversation messages
- `summarize_conversation`: Generate conversation summaries
- `track_conversation_metrics`: Monitor conversation analytics
- `get_conversation_context`: Retrieve recent context
- `reset_conversation`: Clear conversation history

## API Endpoints

### Chat Endpoints (`/api/chat`)

- `POST /api/chat` - Send chat messages (streaming/non-streaming)
- `GET /api/chat/health` - Check chat service health
- `GET /api/chat/kernel-info` - Get kernel configuration info

### Kernel Management (`/api/kernel`)

- `GET /api/kernel/status` - Comprehensive kernel status
- `GET /api/kernel/plugins` - List all registered plugins
- `GET /api/kernel/functions` - List all available functions
- `POST /api/kernel/invoke` - Invoke specific plugin functions
- `GET /api/kernel/health` - Kernel health check

### Conversation Management (`/api/kernel/conversation`)

- `POST /api/kernel/conversation/add-message` - Add message to tracking
- `GET /api/kernel/conversation/summary` - Get conversation summary
- `GET /api/kernel/conversation/metrics` - Get conversation metrics
- `POST /api/kernel/conversation/reset` - Reset conversation history

### Utilities (`/api/kernel/utilities`)

- `POST /api/kernel/utilities/validate-message` - Validate message content

## Configuration

### Environment Variables

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-05-01-preview
```

### Dependencies

Added to `requirements.txt`:
```
semantic-kernel>=1.0.0
azure-identity>=1.15.0
```

## Usage Examples

### Basic Chat with Semantic Kernel

```python
from app.kernel.services.chat_service import get_chat_service

# Get the chat service
chat_service = get_chat_service()

# Send a message
messages = [{"role": "user", "content": "Hello, world!"}]
result = await chat_service.complete_chat(
    messages=messages,
    max_tokens=1000,
    temperature=0.7
)
```

### Plugin Function Invocation

```python
from app.kernel.services.enhanced_kernel_service import get_enhanced_kernel_service

# Get enhanced service
enhanced_service = get_enhanced_kernel_service()

# Invoke a plugin function
result = await enhanced_service.invoke_function(
    plugin_name="ChatUtilities",
    function_name="validate_message",
    message="Hello, world!",
    min_length=1,
    max_length=1000
)
```

### Conversation Tracking

```python
# Track a user message
await enhanced_service.invoke_function(
    plugin_name="Conversation",
    function_name="add_conversation_message",
    role="user",
    content="How can I help you today?",
    tokens=20
)

# Get conversation summary
summary = await enhanced_service.invoke_function(
    plugin_name="Conversation",
    function_name="summarize_conversation",
    max_messages=10
)
```

## Best Practices Implemented

### 1. Security
- **No Hardcoded Credentials**: All credentials from environment variables
- **Input Validation**: Message validation through plugins
- **Error Sanitization**: Safe error messages without exposing internals

### 2. Performance
- **Connection Pooling**: Efficient Azure OpenAI client management
- **Streaming Support**: Real-time response streaming
- **Token Estimation**: Rough token counting for cost optimization
- **Caching**: Singleton pattern for service instances

### 3. Monitoring & Observability
- **Comprehensive Logging**: Structured logging throughout
- **Request Tracking**: Unique request IDs for tracing
- **Conversation Analytics**: Message tracking and metrics
- **Health Checks**: Multiple levels of health monitoring

### 4. Error Handling
- **Graceful Degradation**: Continues working when plugins fail
- **Retry Logic**: Built into Semantic Kernel connectors
- **Detailed Error Information**: Structured error responses
- **Circuit Breaker Pattern**: Prevents cascade failures

### 5. Extensibility
- **Plugin Architecture**: Easy to add new functionality
- **Function Composition**: Combine multiple functions
- **Service Abstraction**: Clean interfaces between layers
- **Configuration Management**: Centralized configuration

## Testing

The implementation includes health check endpoints that can be used to verify:

1. **Kernel Health**: `/api/kernel/health`
2. **Chat Service Health**: `/api/chat/health`
3. **Plugin Functionality**: `/api/kernel/invoke`

Example health check:
```bash
curl http://localhost:3001/api/kernel/health
```

## Migration from Direct OpenAI

The migration maintains backward compatibility:

1. **Same Interface**: Chat endpoints work identically
2. **Enhanced Features**: Additional plugin capabilities
3. **Better Monitoring**: Comprehensive analytics
4. **Future-Proof**: Easy to extend with new AI models

## Troubleshooting

### Common Issues

1. **Configuration Errors**
   - Check environment variables are set correctly
   - Verify Azure OpenAI endpoint and API key
   - Ensure deployment name matches your Azure resource

2. **Plugin Failures**
   - Check `/api/kernel/status` for plugin health
   - Verify function names and parameters
   - Review logs for specific error messages

3. **Performance Issues**
   - Monitor token usage through conversation metrics
   - Check Azure OpenAI quota and limits
   - Review conversation history size

### Debug Endpoints

- `/api/kernel/status` - Full kernel status
- `/api/kernel/functions` - Available functions
- `/api/chat/kernel-info` - Configuration details

This implementation follows Microsoft's Semantic Kernel best practices and provides a robust, extensible foundation for AI-powered chat applications.
