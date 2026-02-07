"""
Inference Service
Core ML inference logic - separated from HTTP layer
This is the BRAIN 🧠 of the system
"""
import numpy as np
from typing import List, Dict
from app.ml.model_loader import ModelLoader
from app.schemas.models import PredictRequest


class InferenceService:
    """
    Handles ML model inference
    Detection ≠ Decision
    """

    def __init__(self):
        self.model_loader = ModelLoader()
        self.model = self.model_loader.model
        self.scaler = self.model_loader.scaler

    def _extract_features(self, request: PredictRequest) -> list[float]:
        """
        Extract features in the EXACT order used during training
        """
        return [
            request.amount_usd,
            request.tx_count_user,
            request.rolling_volume_user,
            request.relative_amount,
        ]

    def run_inference(self, request: PredictRequest) -> float:
        """
        Run inference for a single transaction
        """
        # 1️⃣ Extract features
        features = self._extract_features(request)

        # 2️⃣ Validate feature vector
        self.model_loader.validate_features(features)

        # 3️⃣ Scale
        X_scaled = self.scaler.transform([features])

        # 4️⃣ Isolation Forest score (higher = more anomalous)
        raw_score = -self.model.score_samples(X_scaled)[0]

        return float(raw_score)

    def batch_inference(self, requests: List[PredictRequest]) -> List[float]:
        """
        Batch inference for multiple transactions
        """
        feature_matrix = [self._extract_features(req) for req in requests]

        for features in feature_matrix:
            self.model_loader.validate_features(features)

        X_scaled = self.scaler.transform(feature_matrix)
        raw_scores = -self.model.score_samples(X_scaled)

        return [float(score) for score in raw_scores]

    def explain_features(self, request: PredictRequest) -> Dict[str, float]:
        """
        Return feature values for interpretability
        """
        return {
            "amount_usd": request.amount_usd,
            "tx_count_user": request.tx_count_user,
            "rolling_volume_user": request.rolling_volume_user,
            "relative_amount": request.relative_amount,
        }
