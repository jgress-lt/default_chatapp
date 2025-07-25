# Azure OpenAI Chat Application with Semantic Kernel

A modern chat application that uses Microsoft Semantic Kernel for AI orchestration with Azure OpenAI. Features automatic function calling, real-time streaming responses, and comprehensive logging. Built with React, TypeScript, FastAPI, and Semantic Kernel.

## Project Structure

```
default_chatapp/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/     # React components (Chat, Message, ThemeToggle, Spinner)
│   │   ├── services/       # API and utility services
│   │   └── lib/           # Type definitions
│   ├── public/            # Static assets
│   ├── package.json       # Client dependencies
│   └── vite.config.ts     # Vite configuration
├── server/                 # Backend FastAPI application with Semantic Kernel
│   ├── app/
│   │   ├── routers/       # API route handlers (chat, health, kernel)
│   │   ├── services/      # Semantic Kernel integration services
│   │   ├── middleware/    # Request logging middleware
│   │   ├── config/        # Configuration (logging)
│   │   └── kernel/        # Semantic Kernel components
│   │       ├── config/    # Kernel configuration
│   │       ├── plugins/   # Function plugins (TestPlugin)
│   │       └── services/  # Enhanced kernel services
│   ├── main.py            # FastAPI entry point
│   ├── requirements.txt   # Python dependencies
│   └── .env.local         # Environment variables
├── package.json           # Root workspace configuration
├── README.md
├── TEST_FUNCTION_README.md # Function calling documentation
└── SEMANTIC_KERNEL_README.md # Semantic Kernel guide
```

## Features

- **Modern UI**: Clean design with light/dark theme toggle
- **Real-time Streaming**: Live response streaming from Azure OpenAI via Semantic Kernel
- **Automatic Function Calling**: AI automatically detects when to call functions based on user intent
- **Function Call Transparency**: Shows which functions were called during conversations with execution metadata
- **Local Storage**: Chat history persisted in browser
- **Smart Input**: Enter to send, Shift+Enter for new lines
- **Clear History**: One-click chat history clearing
- **Semantic Kernel Integration**: Microsoft's AI orchestration framework for enhanced capabilities
- **Function Plugins**: Extensible plugin system for custom functions
- **Comprehensive Logging**: Detailed logging of user questions, function calls, and AI responses
- **Full Response Capture**: Complete response content logged to console for both streaming and non-streaming requests
- **Cosmos DB Chat Logging**: User questions and AI responses automatically stored in Cosmos DB for analytics
- **Request Tracking**: Each request gets a unique ID for tracking in logs
- **Error Handling**: Robust error handling and recovery

## Tech Stack

### Frontend (`/client`)
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Framer Motion** for smooth animations
- **Lucide React** for beautiful icons

### Backend (`/server`)
- **FastAPI** (Python) for high-performance API
- **Microsoft Semantic Kernel** for AI orchestration and function calling
- **Azure OpenAI SDK** for AI integration
- **Azure Cosmos DB** for chat and request logging
- **Uvicorn** ASGI server

### AI & Function Calling
- **Semantic Kernel Framework** for automatic function calling
- **Function Plugins** with @kernel_function decorators
- **TestPlugin** with time, math, and statistics functions
- **Enhanced Kernel Service** for plugin management
- **Automatic Intent Detection** for function triggering

## Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+**
- **Azure OpenAI** resource with API key
- **Azure Cosmos DB** account (for logging and chat history)

## Function Calling Demo

This application includes a **TestPlugin** that demonstrates automatic function calling:

### Available Functions
- **get_current_time()** - Triggers when users ask about time/date
  - "What time is it?"
  - "What's the current date?"
  - "Show me the timestamp"

- **calculate_simple_math()** - Triggers when users ask for math calculations
  - "What's 15 + 27?"
  - "Can you multiply 8 by 12?"
  - "Divide 100 by 4"

- **get_plugin_stats()** - Triggers when users ask about plugin usage
  - "How many times have functions been called?"
  - "Show me plugin statistics"

### How It Works
1. User asks a question in natural language
2. AI analyzes the intent using function descriptions
3. Semantic Kernel automatically calls the appropriate function
4. Function executes and returns result
5. AI incorporates the result into a natural response

No manual API calls needed - everything is automatic based on user intent!

## Setup

### 1. Environment Configuration

Create a `.env.local` file in the `/server` directory:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Azure Cosmos DB Configuration
AZURE_COSMOS_DB_NO_SQL_URL=https://your-cosmos-account.documents.azure.com:443/
AZURE_COSMOS_DB_NO_SQL_KEY=your-cosmos-key-here

# Optional: Logging Configuration
LOG_LEVEL=INFO
```

### 2. Install Dependencies

```bash
# Install all dependencies from root directory
npm run install-all

# Or install individually:
npm install                              # Root dependencies
cd client && npm install               # Client dependencies  
cd ../server && pip install -r requirements.txt  # Python dependencies
```

### 3. Run the Application

Start both frontend and backend servers:

```bash
# From root directory - starts both client and server
npm run dev

# Or start individually:
cd client && npm run dev     # Frontend on http://localhost:3000
cd server && python main.py # Backend on http://localhost:3001
```

## Development Scripts

### Root Directory Commands
```bash
npm run dev              # Start both client and server
npm run client           # Start only frontend
npm run python-server    # Start only backend
npm run install-all      # Install all dependencies
npm run build           # Build client for production
npm run preview         # Preview production build
```

### Client Directory (`/client`)
```bash
cd client
npm run dev             # Start Vite dev server
npm run build           # Build for production
npm run preview         # Preview production build
npm run format          # Format code with Prettier
npm run lint            # Lint code with ESLint
```

### Server Directory (`/server`)
```bash
cd server
python main.py          # Start FastAPI server
```

## Function Call Tracking

This application includes comprehensive function call tracking that provides transparency about which functions were executed during conversations.

### How Function Tracking Works

1. **Automatic Detection**: The system automatically tracks when functions are called by the AI during conversations
2. **Execution Metadata**: Captures function name, plugin name, parameters, results, and execution time
3. **Streaming Integration**: Function call information is sent as metadata in the final chunk of streaming responses
4. **Real-time Display**: Function calls are displayed in the UI immediately after the AI response completes

### Function Call Information

For each function call, the system tracks:
- **Function Name**: The specific function that was executed
- **Plugin Name**: Which plugin the function belongs to
- **Parameters**: The parameters passed to the function
- **Result**: The return value from the function
- **Execution Time**: How long the function took to execute (in milliseconds)
- **Call Order**: The sequence in which functions were called
- **Timestamp**: When the function was executed

### Visual Display

Function calls are displayed in a blue info box below the AI response showing:
- Total number of functions called
- List of executed functions with plugin.function() format
- Execution time for each function call
- Clear visual indication that functions were used

### Example Function Calls

Try these questions to see function calling in action:
- "What time is it?" → Calls `TestPlugin.get_current_time()`
- "What's 15 + 27?" → Calls `TestPlugin.calculate_simple_math()`
- "Show me plugin stats" → Calls `TestPlugin.get_plugin_stats()`

### Technical Implementation

- **Backend**: Function call tracker service captures execution metadata
- **Streaming**: Metadata sent as final chunk before completion signal
- **Frontend**: Service parser handles function metadata separately from content
- **UI**: React component displays function information with animations

## Chat Logging & Analytics

The application includes comprehensive chat logging to Cosmos DB for analytics, debugging, and conversation tracking.

### Automatic Chat Storage

Every conversation is automatically logged to Cosmos DB with the following data:

#### Chat Request Documents
- **User Question**: Complete user input for each request
- **Conversation Context**: Full message history leading to the question
- **Request Settings**: Max tokens, temperature, streaming mode
- **Metadata**: Message counts, conversation length, timestamps

#### Chat Response Documents  
- **AI Response**: Complete response content from the AI
- **Performance Metrics**: Processing time, chunk count, response length
- **Function Calls**: Detailed information about any functions called during processing
- **Execution Data**: Timestamps, processing duration, streaming vs non-streaming

#### Document Structure
```json
{
  "id": "chat_request_12345678",
  "type": "chat_request",
  "request_id": "12345678-1234-5678-9012-123456789abc", 
  "user_question": "What time is it?",
  "full_conversation": [...],
  "request_settings": {
    "max_tokens": 1000,
    "temperature": 0.7,
    "is_streaming": true
  }
}
```

### Benefits of Chat Logging

1. **Analytics**: Track conversation patterns and user behavior
2. **Debugging**: Identify issues with specific requests using request IDs
3. **Performance Monitoring**: Analyze response times and processing metrics
4. **Function Usage**: Monitor which AI functions are being called most frequently
5. **Content Analysis**: Review conversation quality and AI response accuracy

### Data Privacy

- User questions and AI responses are stored in your own Cosmos DB instance
- Data remains within your Azure subscription and geographic region
- No data is shared with external services beyond Azure OpenAI for processing

## Usage

1. **Send Messages**: Type your message and press Enter to send
2. **Multi-line Input**: Use Shift+Enter to create new lines
3. **Clear History**: Click the trash icon to clear chat history
4. **Theme Toggle**: Click the theme button to switch between light/dark modes
5. **Function Calling**: Ask questions like "What time is it?" or "What's 5+3?" to see automatic function calling
6. **Request Tracking**: Each request gets a unique ID for tracking in logs
7. **View Logs**: Check the server terminal to see detailed logging of user questions and function calls

## API Endpoints

### Core Endpoints
- `GET /` - Root health check
- `GET /health` - Detailed health status with timestamp
- `POST /api/chat` - Stream chat completions from Azure OpenAI with automatic function calling
- `GET /api/kernel/status` - Semantic Kernel status and plugin information
- `GET /api/kernel/health` - Kernel health check

### Request Format
```json
{
  "messages": [
    {
      "role": "user", 
      "content": "Hello, how are you?"
    }
  ],
  "stream": true,
  "max_tokens": 1000,
  "temperature": 0.7
}
```

### Response Format (Streaming)
```
data: {"choices": [{"delta": {"content": "Hello! I'm"}}]}
data: {"choices": [{"delta": {"content": " doing well"}}]}
data: [DONE]
```

## Architecture

### Semantic Kernel Integration (`/server/app/kernel/`)
- **`config/kernel_config.py`** - Kernel initialization and Azure OpenAI service configuration
- **`plugins/test_plugin.py`** - TestPlugin with @kernel_function decorated methods
- **`services/enhanced_kernel_service.py`** - Plugin management and kernel enhancement
- **`services/chat_service.py`** - Semantic Kernel chat service with function calling

### Frontend Service Layer (`/client/src/services/`)
- **`AzureOpenAIService`** - Handles streaming communication with backend API
- **`ChatStorageService`** - Manages local storage persistence for chat history  
- **`UtilityService`** - Common utility functions (ID generation, etc.)

### Frontend Components (`/client/src/components/`)
- **`Chat`** - Main chat interface with message handling and streaming
- **`Message`** - Individual message display with animations
- **`ThemeToggle`** - Light/dark theme switcher
- **`Spinner`** - Loading animations and indicators

### Backend Architecture (`/server/app/`)
- **`routers/`** - API route handlers for chat, health, and kernel endpoints
- **`services/`** - Chat logging service and Semantic Kernel integration
- **`middleware/`** - HTTP request logging middleware (console only)
- **`config/`** - Application configuration and logging setup

### Function Calling Flow
1. **User Input** → Chat component captures and validates message
2. **API Request** → Frontend sends to FastAPI backend with Semantic Kernel
3. **Intent Analysis** → AI analyzes message for function calling opportunities
4. **Automatic Function Calling** → Semantic Kernel automatically calls appropriate functions
5. **Function Execution** → Plugin functions execute and return results
6. **AI Response** → AI incorporates function results into natural language response
7. **Real-time Updates** → Frontend parses SSE stream and updates UI
8. **Chat Logging** → User questions and AI responses logged to Cosmos DB via chat service

## Deployment

### Frontend Deployment
```bash
cd client
npm run build
# Deploy the 'dist' folder to your hosting service
```

### Backend Deployment
Deploy the FastAPI application (`server/`) to:
- **Azure App Service** (recommended)
- **Azure Container Apps** 
- **Azure Functions** (for serverless)
- Any Python hosting platform

### Environment Variables for Production
```env
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-production-key
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_COSMOS_DB_NO_SQL_URL=https://your-cosmos.documents.azure.com:443/
AZURE_COSMOS_DB_NO_SQL_KEY=your-cosmos-key
LOG_LEVEL=WARNING
```

## Configuration

### Azure OpenAI Settings
- **Endpoint**: Your Azure OpenAI resource endpoint URL
- **API Key**: Authentication key for your Azure OpenAI resource
- **Deployment**: Name of your deployed model (e.g., "gpt-4", "gpt-35-turbo")
- **API Version**: Azure OpenAI API version (default: "2024-12-01-preview")

### Cosmos DB Settings  
- **URL**: Your Cosmos DB account endpoint
- **Key**: Primary or secondary key for authentication
- **Database**: "chatHistoryDb" (created automatically)
- **Containers**: 
  - "chatHistory" - User messages and chat history (not currently used)
  - "requestLogs" - Chat conversations and AI responses (used by chat service)
- **Chat Logging**: Automatic storage of user questions and AI responses via dedicated chat logging service
- **Analytics**: Complete conversation data for performance analysis and debugging

### Logging Configuration
- **LOG_LEVEL**: INFO, DEBUG, WARNING, ERROR, CRITICAL
- **Console Response Capture**: Full AI responses printed to console for both streaming and non-streaming requests
- **Cosmos DB Chat Logging**: Complete conversations automatically stored in Cosmos DB via chat service
- **HTTP Request Logging**: Basic HTTP request/response logging to console via middleware
- **Request Tracking**: Each request gets unique ID for correlation across logs
- **Function Call Logging**: Detailed logging when AI automatically calls functions
- **Performance Metrics**: Processing time, chunk count, and response length tracking

#### Cosmos DB Chat Storage
The chat service automatically stores complete conversations in Cosmos DB with separate documents for:
- **Chat Requests**: User questions, conversation context, and request settings
- **Chat Responses**: AI responses, processing metrics, and function call details

#### Response Logging Format
```
=== STREAMING RESPONSE COMPLETE ===
Request ID: 12345678-1234-5678-9012-123456789abc
Full Response: [Complete response content]
Response Length: 245 characters
Processing Time: 1.23s
Chunks Processed: 15
==================================================
```

### UI Customization
Modify theme colors in `client/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      'neon-pink': '#ff6b9d',
      'neon-blue': '#4ecdc4', 
      'neon-green': '#a8e6cf',
      // ... other custom colors
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend is running on port 3001
   - Check CORS configuration in `server/app/__init__.py`

2. **Environment Variables**
   - Verify `.env.local` file exists in `/server` directory
   - Check all required variables are set correctly
   - Ensure no trailing spaces or quotes in values

3. **Azure OpenAI Errors**
   - Verify endpoint URL format and API key
   - Check deployment name matches your Azure OpenAI model deployment
   - Ensure API version is supported

4. **Cosmos DB Connection**
   - Verify Cosmos DB URL and key are correct
   - Check network connectivity to Azure
   - Ensure Cosmos DB account is active

5. **Dependencies**
   - Run `npm run install-all` from root directory
   - For Python: `cd server && pip install -r requirements.txt`
   - Clear node_modules and reinstall if needed

6. **Function Calling Issues**
   - Check server logs for plugin registration messages
   - Verify TestPlugin is loaded correctly
   - Test with simple questions like "What time is it?"
   - Check Semantic Kernel configuration

### Health Checks
- **Backend Health**: Visit http://localhost:3001/health
- **Root Endpoint**: Visit http://localhost:3001/ 
- **Kernel Status**: Visit http://localhost:3001/api/kernel/status
- **Frontend**: Visit http://localhost:3000

### Debug Logging
- **Enable verbose logging**: Set `LOG_LEVEL=DEBUG` in `.env.local`
- **Response capture**: Full AI responses are automatically printed to console for all requests
- **Function call tracking**: All AI function calls are logged with execution details
- **Request correlation**: Each request gets a unique ID for tracking across logs

## Dependencies

### Frontend Dependencies
- React 18, TypeScript, Vite
- Tailwind CSS, Framer Motion, Lucide React
- All managed via npm

### Backend Dependencies  
- FastAPI, Uvicorn, Microsoft Semantic Kernel
- Azure OpenAI SDK, Azure Cosmos DB SDK
- python-dotenv, semantic-kernel
- All listed in `requirements.txt`

## Additional Documentation

- **TEST_FUNCTION_README.md** - Detailed guide to automatic function calling
- **SEMANTIC_KERNEL_README.md** - Semantic Kernel integration guide

## License

MIT License - see LICENSE file for details.
