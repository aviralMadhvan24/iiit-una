from pydantic import BaseModel
from datetime import datetime

class SimulatedTransaction(BaseModel):
    tx_hash: str
    wallet_address: str
    amount_usd: float
    gas_price: float
    slippage: float
    timestamp: datetime
