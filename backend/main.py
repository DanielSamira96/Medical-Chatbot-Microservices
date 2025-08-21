"""
FastAPI Medical Chatbot Application

Main application file for the stateless medical chatbot microservice.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from backend.api.user_info import router as user_info_router
from backend.api.medical_qa import router as medical_qa_router
from backend.api.health import router as health_router
from backend.utils.error_handlers import (
    ErrorHandlingMiddleware, 
    create_http_exception_handler,
    create_validation_exception_handler
)
from config.settings import settings
from utils.logging import logger, log_system_startup

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting Medical Chatbot Microservice...")
    log_system_startup()
    
    # Validate Azure OpenAI configuration
    config_result = settings.validate_azure_config()
    if not config_result['valid']:
        invalid = config_result.get('invalid_fields', [])
        logger.error(f"Azure OpenAI configuration incomplete: {', '.join(invalid)}")
        print(f"ERROR: Azure OpenAI configuration incomplete: {', '.join(invalid)}")
    else:
        logger.info("Azure OpenAI configuration validated successfully")
        print("Azure OpenAI configuration validated successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medical Chatbot Microservice...")
    print("Shutting down Medical Chatbot Microservice...")

# Create FastAPI application
app = FastAPI(
    title="Medical Chatbot Microservice",
    description="Stateless microservice for Israeli medical services chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add error handling middleware
app.add_middleware(ErrorHandlingMiddleware)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom exception handlers
app.add_exception_handler(HTTPException, create_http_exception_handler())
app.add_exception_handler(RequestValidationError, create_validation_exception_handler())

# Include API routers
app.include_router(health_router, prefix=f"/api/{settings.API_VERSION}", tags=["Health"])
app.include_router(user_info_router, prefix=f"/api/{settings.API_VERSION}", tags=["User Information"])
app.include_router(medical_qa_router, prefix=f"/api/{settings.API_VERSION}", tags=["Medical Q&A"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Medical Chatbot Microservice",
        "api_version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn

    print(f"Starting server on {settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(
        "backend.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        # reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )