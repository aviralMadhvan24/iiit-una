import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

DATA_PATH = "aviral.csv"
FEATURES = [
    "amount_usd",
    "tx_count_user",
    "rolling_volume_user",
    "relative_amount"
]

df = pd.read_csv(DATA_PATH)

df = df.dropna()
df = df[df["amount_usd"] > 0]
df = df[np.isfinite(df).all(axis=1)]

print("✅ Data loaded and validated")
print(df.describe())

train_df = df[
    (df["amount_usd"] < df["amount_usd"].quantile(0.99)) &
    (df["relative_amount"] < df["relative_amount"].quantile(0.99))
]

print(f"Rows before filtering: {len(df)}")
print(f"Rows after filtering: {len(train_df)}")


scaler = StandardScaler()
X_train = scaler.fit_transform(train_df[FEATURES])

joblib.dump(scaler, "scaler.pkl")
print("✅ scaler.pkl saved")


model = IsolationForest(
    n_estimators=300,
    max_samples=0.8,
    contamination="auto",
    random_state=42
)

model.fit(X_train)
joblib.dump(model, "model.pkl")
print("✅ model.pkl saved")


X_all = scaler.transform(df[FEATURES])
df["risk_score"] = -model.score_samples(X_all)

threshold = df["risk_score"].quantile(0.98)
df["alert"] = df["risk_score"] > threshold

print("\nAlert distribution:")
print(df["alert"].value_counts(normalize=True))
print(f"\nThreshold used: {threshold}")

df.to_csv("scored_transactions.csv", index=False)
print("✅ scored_transactions.csv saved")


with open("threshold.txt", "w") as f:
    f.write(str(threshold))

print("✅ threshold.txt saved")
