"""
FastAPI application for address book management.
"""

import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import addresses

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with coordinate-based search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers
app.include_router(addresses.router)

# Initialize database on startup


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    logger.info("Starting Address Book API...")
    init_db()
    logger.info("Application started successfully")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint providing API information."""
    return {"message": "Welcome to Address Book API", "docs": "/docs", "redoc": "/redoc"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "An internal server error occurred"})
