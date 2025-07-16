# Azure OpenAI Chat Application

A modern, lightweight chat application that connects to Azure OpenAI's Chat Completions API with real-time streaming responses. Built with React, TypeScript, and FastAPI.

## 📁 Project Structure

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
├── server/                 # Backend FastAPI application
│   ├── app/
│   │   ├── routers/       # API route handlers (chat, health)
│   │   ├── services/      # Business logic (Azure OpenAI integration)
│   │   ├── middleware/    # Request logging middleware
│   │   └── config/        # Configuration (logging)
│   ├── main.py            # FastAPI entry point
│   ├── requirements.txt   # Python dependencies
│   └── .env.local         # Environment variables
├── package.json           # Root workspace configuration
└── README.md
```

## ✨ Features

- 🎨 **Beautiful UI**: Modern design with light/dark theme toggle
- ⚡ **Real-time Streaming**: Live response streaming from Azure OpenAI
- 💾 **Local Storage**: Chat history persisted in browser
- 🎯 **Smart Input**: Enter to send, Shift+Enter for new lines
- 🗑️ **Clear History**: One-click chat history clearing
- 🔧 **Clean Architecture**: Modular service-based design
- 📊 **Request Logging**: Comprehensive logging to Cosmos DB
- 🛡️ **Error Handling**: Robust error handling and recovery

## 🛠️ Tech Stack

### Frontend (`/client`)
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Framer Motion** for smooth animations
- **Lucide React** for beautiful icons

### Backend (`/server`)
- **FastAPI** (Python) for high-performance API
- **Azure OpenAI SDK** for AI integration
- **Azure Cosmos DB** for chat and request logging
- **Uvicorn** ASGI server

## 🚀 Prerequisites

- **Node.js 18+** and npm
- **Python 3.8+**
- **Azure OpenAI** resource with API key
- **Azure Cosmos DB** account (for logging and chat history)

## ⚙️ Setup

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

## 📜 Development Scripts

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

## 🎯 Usage

1. **Send Messages**: Type your message and press Enter to send
2. **Multi-line Input**: Use Shift+Enter to create new lines
3. **Clear History**: Click the trash icon to clear chat history
4. **Theme Toggle**: Click the theme button to switch between light/dark modes
5. **Request Tracking**: Each request gets a unique ID for tracking in logs

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Root health check
- `GET /health` - Detailed health status with timestamp
- `POST /api/chat` - Stream chat completions from Azure OpenAI

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

## 🏗️ Architecture

### Frontend Service Layer (`/client/src/services/`)
- **`AzureOpenAIService`** - Handles streaming communication with Azure OpenAI API
- **`ChatStorageService`** - Manages local storage persistence for chat history  
- **`UtilityService`** - Common utility functions (ID generation, etc.)

### Frontend Components (`/client/src/components/`)
- **`Chat`** - Main chat interface with message handling and streaming
- **`Message`** - Individual message display with animations
- **`ThemeToggle`** - Light/dark theme switcher
- **`Spinner`** - Loading animations and indicators

### Backend Architecture (`/server/app/`)
- **`routers/`** - API route handlers for chat and health endpoints
- **`services/`** - Business logic for Azure OpenAI integration
- **`middleware/`** - Request logging and tracking middleware
- **`config/`** - Application configuration and logging setup

### Data Flow
1. **User Input** → Chat component captures and validates
2. **API Request** → AzureOpenAIService sends to FastAPI backend  
3. **Azure OpenAI** → Backend streams response from Azure OpenAI
4. **Real-time Updates** → Frontend parses SSE stream and updates UI
5. **Persistence** → Chat history saved to localStorage and requests logged to Cosmos DB

## 🚀 Deployment

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

## ⚙️ Configuration

### Azure OpenAI Settings
- **Endpoint**: Your Azure OpenAI resource endpoint URL
- **API Key**: Authentication key for your Azure OpenAI resource
- **Deployment**: Name of your deployed model (e.g., "gpt-4", "gpt-35-turbo")
- **API Version**: Azure OpenAI API version (default: "2024-12-01-preview")

### Cosmos DB Settings  
- **URL**: Your Cosmos DB account endpoint
- **Key**: Primary or secondary key for authentication
- **Database**: "chatHistoryDb" (created automatically)
- **Containers**: "chatHistory" and "requestLogs" (created automatically)

### Logging Configuration
- **LOG_LEVEL**: INFO, DEBUG, WARNING, ERROR, CRITICAL
- Console-only logging (no local files)
- Request/response logging to Cosmos DB with unique request IDs

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

## 🔧 Troubleshooting

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

### Health Checks
- **Backend Health**: Visit http://localhost:3001/health
- **Root Endpoint**: Visit http://localhost:3001/ 
- **Frontend**: Visit http://localhost:3000

### Debug Logging
Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env.local`

## 📋 Dependencies

### Frontend Dependencies
- React 18, TypeScript, Vite
- Tailwind CSS, Framer Motion, Lucide React
- All managed via npm

### Backend Dependencies  
- FastAPI, Uvicorn, Azure OpenAI SDK
- Azure Cosmos DB SDK, python-dotenv
- All listed in `requirements.txt`

## 📄 License

MIT License - see LICENSE file for details.
