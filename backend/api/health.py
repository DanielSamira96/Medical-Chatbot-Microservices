"""
Health check API endpoints.
"""

from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import Response
from backend.models.schemas import HealthCheckResponse
from config.settings import settings
from utils.helpers import get_available_contexts

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify system status.
    
    Returns information about:
    - Service status
    - Azure OpenAI configuration
    - Available user contexts
    """
    
    try:
        # Check Azure OpenAI configuration
        config_result = settings.validate_azure_config()
        azure_configured = config_result['valid']
        
        # Get available user contexts
        available_contexts = get_available_contexts(settings.DATA_FOLDER)
        context_names = [f"{hmo}_{tier}" for hmo, tier in available_contexts]
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            azure_openai_configured=azure_configured,
            available_contexts=context_names
        )
        
    except Exception as e:
        print(f"Health check error: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            azure_openai_configured=False,
            available_contexts=[]
        )

@router.get("/favicon.ico")
async def favicon():
    """Handle favicon requests."""
    return Response(status_code=204)  # No Content