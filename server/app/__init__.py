import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, health, kernel
from .middleware.logging_middleware import RequestLoggingMiddleware
from .config.logging_config import setup_logging

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '.env.local')
load_dotenv(env_path)

# Setup comprehensive logging
setup_logging()

# Get logger for this module
logger = logging.getLogger("backend.app")

# Initialize Cosmos DB client for simple chat history storage
COSMOS_URL = os.getenv('AZURE_COSMOS_DB_NO_SQL_URL')
COSMOS_KEY = os.getenv('AZURE_COSMOS_DB_NO_SQL_KEY')

logger.info("Initializing Cosmos DB client")
logger.info(f"Cosmos DB URL: {COSMOS_URL[:50]}..." if COSMOS_URL else "Cosmos DB URL: NOT SET")

# Initialize Cosmos DB client
cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
database = cosmos_client.create_database_if_not_exists(id="chatHistoryDb")
container = database.create_container_if_not_exists(
    id="chatHistory",
    partition_key=PartitionKey(path="/sessionId"),
    offer_throughput=400
)

# Create container for request logging
request_logs_container = database.create_container_if_not_exists(
    id="requestLogs",
    partition_key=PartitionKey(path="/sessionId"),
    offer_throughput=400
)

logger.info("Cosmos DB client initialized successfully")

def create_app() -> FastAPI:
    logger.info("Creating FastAPI application")
    
    app = FastAPI(title="Azure Chat API", version="1.0")

    # Add request logging middleware (before CORS)
    logger.info("Adding request logging middleware")
    app.add_middleware(RequestLoggingMiddleware)

    logger.info("Adding CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    logger.info("Including routers")
    app.include_router(chat)
    app.include_router(health)
    app.include_router(kernel)
    
    logger.info("FastAPI application created successfully")
    return app

app = create_app()
