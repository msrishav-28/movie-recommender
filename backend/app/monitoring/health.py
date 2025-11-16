"""
Health check endpoints for monitoring.
"""

from fastapi import APIRouter, status
from typing import Dict, Any
import time
from datetime import datetime

from app.db.database import get_db_health
from app.core.config import settings

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    Returns 200 if service is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check including all services.
    """
    start_time = time.time()
    
    # Check database
    db_health = await get_db_health()
    
    # TODO: Check Redis
    redis_health = {"status": "not_implemented"}
    
    # TODO: Check Pinecone
    pinecone_health = {"status": "not_implemented"}
    
    # TODO: Check Elasticsearch
    elasticsearch_health = {"status": "not_implemented"}
    
    # Overall status
    all_healthy = db_health.get("status") == "healthy"
    
    duration_ms = (time.time() - start_time) * 1000
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {
            "database": db_health,
            "redis": redis_health,
            "pinecone": pinecone_health,
            "elasticsearch": elasticsearch_health
        },
        "response_time_ms": round(duration_ms, 2)
    }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> Dict[str, str]:
    """
    Kubernetes readiness probe.
    Returns 200 if service can accept traffic.
    """
    # Check critical dependencies
    db_health = await get_db_health()
    
    if db_health.get("status") != "healthy":
        return {"status": "not_ready", "reason": "database_unavailable"}
    
    return {"status": "ready"}


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """
    Kubernetes liveness probe.
    Returns 200 if service should stay alive.
    """
    return {"status": "alive"}
