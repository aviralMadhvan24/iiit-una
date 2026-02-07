import pandas as pd

df = pd.read_csv("scored_transactions.csv")

FEATURES = [
    "amount_usd",
    "tx_count_user",
    "rolling_volume_user",
    "relative_amount"
]

print("\n📊 Behavioral Validation (Mean Values)\n")
print(df.groupby("alert")[FEATURES].mean())

print("\n✅ Validation complete")
print("Alerted transactions should show higher economic magnitude.")
