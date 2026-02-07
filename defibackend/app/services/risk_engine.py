def score_transaction(tx):
    score = 0

    if tx.amount_usd > 100_000:
        score += 40
    if tx.gas_price > 150:
        score += 30
    if tx.slippage > 10:
        score += 30

    return min(score, 100)
