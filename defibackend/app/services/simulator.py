import random
import uuid
from datetime import datetime
from app.models.simulated_tx import SimulatedTransaction

WALLETS = [
    "0x81fA...a12",
    "0x9BcD...f32",
    "0xA91E...9a1",
    "0xD34B...88e",
]

def generate_transaction():
    is_malicious = random.random() < 0.25  # 25% malicious

    if is_malicious:
        return SimulatedTransaction(
            tx_hash=str(uuid.uuid4()),
            wallet_address=random.choice(WALLETS),
            amount_usd=random.uniform(100_000, 2_000_000),
            gas_price=random.uniform(200, 500),
            slippage=random.uniform(15, 40),
            timestamp=datetime.utcnow(),
        )
    else:
        return SimulatedTransaction(
            tx_hash=str(uuid.uuid4()),
            wallet_address=random.choice(WALLETS),
            amount_usd=random.uniform(50, 2_000),
            gas_price=random.uniform(20, 80),
            slippage=random.uniform(0.1, 1.5),
            timestamp=datetime.utcnow(),
        )
