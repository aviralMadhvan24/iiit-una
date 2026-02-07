"""
Health check endpoints
System status and readiness checks
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.ml.model_loader import ModelLoader
from app.web3.client import Web3Client
from config.settings import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check - is the service running?
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.MODEL_VERSION
    }

@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - are all dependencies ready?
    Checks: ML model loaded, Web3 connection, etc.
    """
    checks = {
        "model_loaded": False,
        "scaler_loaded": False,
        "web3_connected": False
    }
    
    try:
        # Check ML components
        model_loader = ModelLoader()
        checks["model_loaded"] = model_loader.model is not None
        checks["scaler_loaded"] = model_loader.scaler is not None
        
        # Check Web3 connection
        web3_client = Web3Client()
        checks["web3_connected"] = web3_client.is_connected()
        
        all_ready = all(checks.values())
        
        return {
            "ready": all_ready,
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service not ready: {str(e)}"
        )

@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - can the service respond to requests?
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }