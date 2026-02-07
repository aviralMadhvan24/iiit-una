from app.services.risk_engine import score_transaction
from app.db.database import DatabaseService

db = DatabaseService()

def process_transaction(tx):
    score = score_transaction(tx)
    risk_level = "critical" if score >= 90 else "high" if score >= 70 else "low"
    is_alert = score >= 70

    # ✅ STORE EVERY TRANSACTION
    db.store_simulated_prediction(
        tx_hash=tx.tx_hash,
        wallet_address=tx.wallet_address,
        amount_usd=tx.amount_usd,
        risk_score=score / 100,
        risk_level=risk_level,
        timestamp=tx.timestamp,
        is_alert=is_alert,
    )

    # 🚨 STORE ALERT ONLY IF RISKY
    if is_alert:
        db.store_simulated_alert(
            tx_hash=tx.tx_hash,
            wallet_address=tx.wallet_address,
            amount_usd=tx.amount_usd,
            risk_score=score / 100,
            risk_level=risk_level,
            timestamp=tx.timestamp,
        )
