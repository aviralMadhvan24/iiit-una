ALERTS = []

def process_transaction(tx):
    score = 0

    if tx.amount_usd > 100_000:
        score += 40
    if tx.gas_price > 150:
        score += 30
    if tx.slippage > 10:
        score += 30

    if score >= 70:
        ALERTS.append({
            "id": len(ALERTS) + 1,
            "wallet_address": tx.wallet_address,
            "amount_usd": tx.amount_usd,
            "risk_score": score / 100,
            "risk_level": "critical" if score > 90 else "high",
            "timestamp": tx.timestamp.isoformat(),
        })
