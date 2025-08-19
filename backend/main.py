"""
FastAPI Medical Chatbot Application

Main application file for the stateless medical chatbot microservice.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.api.user_info import router as user_info_router
from backend.api.medical_qa import router as medical_qa_router
from backend.api.health import router as health_router
from config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting Medical Chatbot Microservice...")
    
    # Validate Azure OpenAI configuration
    if not settings.validate_azure_config():
        print("WARNING: Azure OpenAI configuration incomplete!")
    else:
        print("Azure OpenAI configuration validated successfully")
    
    yield
    
    # Shutdown
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

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(user_info_router, prefix="/api/v1", tags=["User Information"])
app.include_router(medical_qa_router, prefix="/api/v1", tags=["Medical Q&A"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Medical Chatbot Microservice",
        "version": "1.0.0",
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
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )