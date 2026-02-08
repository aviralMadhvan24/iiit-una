from app.db.database import DatabaseService

db = DatabaseService()

db.save_telegram_chat_id(
    wallet_address="0x81fA91bA1234567890a",
    telegram_chat_id="6086183340"
)

print("✅ Telegram chat ID registered")
