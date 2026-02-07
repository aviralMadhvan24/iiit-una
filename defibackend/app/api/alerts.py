from fastapi import APIRouter, HTTPException
from typing import Optional

from app.db.database import DatabaseService
from app.schemas.models import RiskLevel

router = APIRouter(prefix="/alerts", tags=["Alerts"])

db_service = DatabaseService()


@router.get("")
def get_alerts(
    page: int = 1,
    page_size: int = 100,
    wallet_address: Optional[str] = None,
    risk_level: Optional[RiskLevel] = None,
):
    skip = (page - 1) * page_size

    alerts = db_service.get_alerts(
        skip=skip,
        limit=page_size,
        wallet_address=wallet_address,
        risk_level=risk_level,
    )

    total = len(
        db_service.get_alerts(
            skip=0,
            limit=10_000,
            wallet_address=wallet_address,
            risk_level=risk_level,
        )
    )

    return {
        "alerts": alerts,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


# 🔥 THIS WAS BROKEN — FIXED VERSION
@router.get("/stats")
def get_alert_stats():
    """
    Return system-wide alert statistics.
    NO parameters. NO body.
    """
    try:
        stats = db_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch stats: {str(e)}",
        )
