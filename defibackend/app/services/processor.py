import asyncio
from app.services.risk_engine import score_transaction
from app.db.database import DatabaseService
from app.notifications.telegram_service import notify_telegram
from app.schemas.models import AlertRecord, RiskLevel

db = DatabaseService()


def process_transaction(tx):
    score = score_transaction(tx)  # 0–100
    risk_score = score / 100

    if score >= 90:
        risk_level = RiskLevel.CRITICAL
    elif score >= 70:
        risk_level = RiskLevel.HIGH
    else:
        risk_level = RiskLevel.LOW

    is_alert = score >= 70

    # ✅ Store prediction
    db.store_simulated_prediction(
        tx_hash=tx.tx_hash,
        wallet_address=tx.wallet_address,
        amount_usd=tx.amount_usd,
        risk_score=risk_score,
        risk_level=risk_level.value,
        timestamp=tx.timestamp,
        is_alert=is_alert,
    )

    if not is_alert:
        return

    # ✅ Store alert
    db.store_simulated_alert(
        tx_hash=tx.tx_hash,
        wallet_address=tx.wallet_address,
        amount_usd=tx.amount_usd,
        risk_score=risk_score,
        risk_level=risk_level.value,
        timestamp=tx.timestamp,
    )

    chat_id = db.get_telegram_chat_id(tx.wallet_address)

    if not chat_id:
        print(f"ℹ️ No Telegram mapping for {tx.wallet_address}")
        return

    alert = AlertRecord(
        tx_hash=tx.tx_hash,
        wallet_address=tx.wallet_address,
        risk_score=risk_score,
        risk_level=risk_level,
        amount_usd=tx.amount_usd,
        timestamp=tx.timestamp,
    )

    # ✅ SAFE async execution (WORKS)
    loop = asyncio.get_event_loop()
    loop.create_task(notify_telegram(chat_id, alert))
