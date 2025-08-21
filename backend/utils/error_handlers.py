"""
Comprehensive error handling middleware for FastAPI.
"""

from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logging import logger, log_error


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to handle all unhandled exceptions."""
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Log incoming request
            logger.api_request(
                endpoint=str(request.url.path),
                method=request.method,
                client_ip=request.client.host if request.client else "unknown",
                user_agent=request.headers.get("user-agent", "unknown")
            )
            
            start_time = datetime.now()
            response = await call_next(request)
            end_time = datetime.now()
            
            # Log successful response
            response_time_ms = (end_time - start_time).total_seconds() * 1000
            logger.api_response(
                endpoint=str(request.url.path),
                status_code=response.status_code,
                response_time_ms=response_time_ms
            )
            
            return response
            
        except HTTPException as e:
            # Log HTTP exceptions
            log_error(
                f"HTTP Exception: {e.status_code} - {e.detail}",
                endpoint=str(request.url.path),
                method=request.method,
                status_code=e.status_code
            )
            raise
            
        except Exception as e:
            # Log unhandled exceptions
            print(f"*** EXCEPTION CAUGHT IN MIDDLEWARE: {type(e).__name__}: {str(e)} ***")
            log_error(
                f"Unhandled exception in {request.method} {request.url.path}",
                exception=e,
                endpoint=str(request.url.path),
                method=request.method,
                client_ip=request.client.host if request.client else "unknown"
            )
            
            # Return generic error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url.path)
                }
            )


def create_http_exception_handler():
    """Create custom HTTP exception handler."""
    
    async def http_exception_handler(request: Request, exc: HTTPException):
        log_error(
            f"HTTP Exception: {exc.status_code}",
            endpoint=str(request.url.path),
            method=request.method,
            status_code=exc.status_code,
            detail=exc.detail
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Request failed",
                # "message": exc.detail,
                "message": str(exc),
                "status_code": exc.status_code,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path)
            }
        )
    
    return http_exception_handler


def create_validation_exception_handler():
    """Create custom validation exception handler."""
    
    async def validation_exception_handler(request: Request, exc):
        log_error(
            "Validation error",
            endpoint=str(request.url.path),
            method=request.method,
            validation_errors=[
                {"field": error["loc"], "message": str(error["msg"])} 
                for error in exc.errors()
            ]
        )
        
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed",
                "message": "The provided data is invalid",
                "details": [
                    {"field": error["loc"], "message": str(error["msg"])}
                    for error in exc.errors()
                ],
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path)
            }
        )
    
    return validation_exception_handler