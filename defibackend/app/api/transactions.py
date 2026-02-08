from fastapi import APIRouter
from app.db.database import DatabaseService

router = APIRouter(prefix="/transactions")
db = DatabaseService()

@router.get("/recent")
def get_recent_transactions(limit: int = 50):
    session = db.SessionLocal()
    try:
        rows = session.execute(
            """
            SELECT tx_hash, wallet_address, amount_usd, risk_score, risk_level, timestamp
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT :limit
            """,
            {"limit": limit},
        ).fetchall()

        return [
            {
                "tx_hash": r[0],
                "wallet_address": r[1],
                "amount_usd": r[2],
                "risk_score": r[3],
                "risk_level": r[4],
                "timestamp": r[5],
            }
            for r in rows
        ]
    finally:
        session.close()
