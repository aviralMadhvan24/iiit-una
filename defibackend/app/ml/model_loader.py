import joblib
from pathlib import Path

# Absolute path to app/
APP_DIR = Path(__file__).resolve().parent.parent

# app/models/
MODEL_DIR = APP_DIR / "models"

MODEL_PATH = MODEL_DIR / "isolation_forest.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

FEATURES = [
    "amount_usd",
    "tx_count_user",
    "rolling_volume_user",
    "relative_amount",
]


class ModelLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        ...
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def validate_features(self, features: list[float]):
        if len(features) != 4:
            raise ValueError(
                f"Expected 4 features, got {len(features)}"
            )
