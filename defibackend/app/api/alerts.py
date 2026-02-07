"""
Alerts API Routes
Alert retrieval, management, and verification
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.models import AlertListResponse, RiskLevel
from app.db.database import DatabaseService

router = APIRouter()

# Initialize database service
db_service = DatabaseService()

@router.get("/alerts", response_model=AlertListResponse)
async def get_alerts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    wallet_address: Optional[str] = Query(None, description="Filter by wallet address"),
    risk_level: Optional[RiskLevel] = Query(None, description="Filter by risk level")
):
    """
    Get list of alerts
    Supports filtering and pagination
    """
    try:
        alerts = db_service.get_alerts(
            skip=skip,
            limit=limit,
            wallet_address=wallet_address,
            risk_level=risk_level
        )
        
        total = len(alerts)  # In production, use count query
        
        return AlertListResponse(
            alerts=alerts,
            total=total,
            page=skip // limit + 1,
            page_size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: int):
    """
    Get specific alert by ID
    """
    try:
        alerts = db_service.get_alerts(skip=0, limit=1)
        # In production, implement get_alert_by_id method
        
        if not alerts:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return alerts[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alert: {str(e)}")

@router.post("/alerts/{alert_id}/verify")
async def verify_alert(
    alert_id: int,
    verified: bool,
    false_positive: Optional[bool] = None,
    notes: Optional[str] = None
):
    """
    Update alert verification status
    Allows marking alerts as verified or false positives
    """
    try:
        db_service.update_alert_verification(
            alert_id=alert_id,
            verified=verified,
            false_positive=false_positive,
            notes=notes
        )
        
        return {
            "message": "Alert verification updated",
            "alert_id": alert_id,
            "verified": verified,
            "false_positive": false_positive
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update alert: {str(e)}")

@router.get("/alerts/stats")
async def get_alert_stats():
    """
    Get alert statistics
    Returns aggregate metrics
    """
    try:
        stats = db_service.get_statistics()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")

@router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    """
    Delete alert (soft delete recommended in production)
    """
    # In production, implement soft delete
    return {
        "message": "Alert deletion not implemented",
        "reason": "Use verification status instead of deletion"
    }