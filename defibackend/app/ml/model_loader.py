import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "isolation_forest.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

FEATURES = [
    "amount_usd",
    "tx_count_user",
    "rolling_volume_user",
    "relative_amount",
]


class ModelLoader:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)
