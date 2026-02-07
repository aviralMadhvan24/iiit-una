import random
import uuid
from datetime import datetime
from app.schemas.simulated_tx import SimulatedTransaction

WALLETS = [
    "0x81fA91bA1234567890a",
    "0x9BcD88Ef4567890123b",
    "0xA91EaaBB8899001122c",
    "0xD34BccDD77889900dd4",
]

def generate_transaction():
    is_malicious = random.random() < 0.25

    return SimulatedTransaction(
        tx_hash=str(uuid.uuid4()),
        wallet_address=random.choice(WALLETS),
        amount_usd=random.uniform(100_000, 2_000_000) if is_malicious else random.uniform(50, 3_000),
        gas_price=random.uniform(200, 500) if is_malicious else random.uniform(20, 80),
        slippage=random.uniform(15, 40) if is_malicious else random.uniform(0.1, 2.0),
        timestamp=datetime.utcnow(),
    )
