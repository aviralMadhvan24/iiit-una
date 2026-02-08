from app.schemas.models import AlertRecord
from app.notifications.telegram_client import TelegramClient
from config.settings import settings

telegram = None

def get_telegram():
    global telegram
    if telegram is None:
        telegram = TelegramClient()
    return telegram


def format_alert(alert: AlertRecord) -> str:
    return f"""
🚨 *DEFI RISK ALERT*

⚠️ *Severity:* {alert.risk_level.upper()}
💰 *Amount:* ${alert.amount_usd:,.2f}
📊 *Risk Score:* {alert.risk_score:.3f}

👛 *Wallet:* `{alert.wallet_address}`
🕒 *Time:* {alert.timestamp.isoformat()}
"""


async def notify_telegram(chat_id: str, alert: AlertRecord):
    if not settings.TELEGRAM_BOT_TOKEN:
        print("ℹ️ Telegram disabled")
        return

    try:
        telegram = get_telegram()
        await telegram.send_message(chat_id, format_alert(alert))
        print(f"✅ Telegram alert sent to {chat_id}")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
