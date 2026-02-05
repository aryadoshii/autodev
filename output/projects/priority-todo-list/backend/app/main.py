"""
Priority Todo List - FastAPI Main Application

A comprehensive task management application that allows users to create,
organize, and track their daily tasks with due dates, completion status,
and priority levels to improve productivity and time management.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from api.auth import router as auth_router
from api.users import router as users_router
from api.tasks import router as tasks_router
from core.config import settings
from core.logging_config import setup_logging
from core.database import init_db


# Configure logging
setup_logging()

# Create logger
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    This context manager handles database initialization on startup
    and cleanup operations on shutdown.
    """
    logger.info("Starting up Priority Todo List application...")
    
    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    logger.info("Shutting down Priority Todo List application...")


# Create FastAPI application with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    description="A comprehensive task management application for organizing daily tasks with priorities and due dates.",
    version="1.0.0"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"]
)


# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(tasks_router, prefix=settings.API_V1_STR)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/", response_model=Dict[str, Any])
async def root() -> Dict[str, Any]:
    """
    Root endpoint providing basic information about the application.
    
    Returns:
        Dictionary containing application information
    """
    return {
        "message": "Welcome to Priority Todo List API",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify application status.
    
    Returns:
        Dictionary containing health status information
    """
    return {
        "status": "healthy",
        "database": "connected",
        "service": "running"
    }


if __name__ == "__main__":
    import uvicorn
    
    # For development purposes only
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )