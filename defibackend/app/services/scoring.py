import numpy as np
from typing import Dict
from app.schemas.models import RiskLevel


class ScoringService:
    """
    Converts raw risk scores into actionable decisions
    Detection ≠ Decision (good architecture)
    """

    def __init__(self):
        # Hackathon-safe fixed thresholds
        self.alert_threshold = 0.98  # top 2% anomalies

    def classify_risk_level(self, risk_score: float) -> RiskLevel:
        if risk_score >= 0.97:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.90:
            return RiskLevel.HIGH
        elif risk_score >= 0.70:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def should_alert(self, risk_score: float) -> bool:
        return risk_score >= self.alert_threshold

    def calculate_confidence(self, risk_score: float) -> float:
        deviation = abs(risk_score - 0.5)
        confidence = 0.5 + deviation
        return float(np.clip(confidence, 0, 1))

    def get_threshold_info(self) -> Dict[str, float]:
        return {
            "alert_threshold": self.alert_threshold,
            "critical_threshold": 0.97,
            "high_threshold": 0.90,
            "medium_threshold": 0.70,
        }
