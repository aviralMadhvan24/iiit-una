from app.notifications.telegram_client import TelegramClient
from app.schemas.models import AlertRecord

telegram = TelegramClient()

def format_alert(alert: AlertRecord) -> str:
    return f"""
🚨 *DEFI RISK ALERT*

⚠️ *Severity:* {alert.risk_level.upper()}
💰 *Amount:* ${alert.amount_usd:,.2f}
📊 *Risk Score:* {alert.risk_score:.3f}

👛 *Wallet:* `{alert.wallet_address}`
🕒 *Time:* {alert.timestamp.isoformat()}

🔎 Action: Manual review recommended
"""

async def notify_telegram(chat_id: str, alert: AlertRecord):
    message = format_alert(alert)
    await telegram.send_message(chat_id, message)
