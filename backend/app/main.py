"""
FastAPI Main Application
Production-grade movie recommendation backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.middleware import setup_middleware
from app.core.logging import setup_logging
from app.db.database import init_db, close_db, check_db_connection
from app.api.v1.router import api_router
from app.monitoring.health import router as health_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for startup and shutdown.
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Check database connection
    db_healthy = await check_db_connection()
    if not db_healthy:
        logger.error("Database connection failed!")
    else:
        logger.info("Database connection established")
    
    # Initialize database tables (development only)
    if settings.DEBUG:
        logger.warning("DEBUG mode: Initializing database tables")
        await init_db()
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_db()
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered movie recommendation system with semantic aesthetic search",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": f"{settings.API_PREFIX}/docs" if settings.DEBUG else "disabled"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS if not settings.RELOAD else 1,
        log_level=settings.LOG_LEVEL.lower()
    )
