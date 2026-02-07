"""
Pydantic schemas for request/response validation
Clean API contracts and type safety
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    """Risk classification levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PredictRequest(BaseModel):
    """
    Request schema for transaction risk prediction
    All features required for model inference
    """
    amount_usd: float = Field(..., gt=0, description="Transaction amount in USD")
    whale_tx: int = Field(..., ge=0, le=1, description="Binary flag: 1 if whale transaction, 0 otherwise")
    tx_count_user: int = Field(..., ge=0, description="Total transaction count by this wallet")
    rolling_volume_user: float = Field(..., ge=0, description="Recent volume surge for this wallet")
    
    # Optional metadata (not used in model)
    tx_hash: Optional[str] = Field(None, description="Transaction hash for reference")
    wallet_address: Optional[str] = Field(None, description="Wallet address for tracking")
    
    @field_validator('amount_usd')
    @classmethod
    def validate_amount(cls, v):
        if v > 1e12:  # Sanity check: $1 trillion
            raise ValueError("Amount exceeds reasonable bounds")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "amount_usd": 500000.0,
                "whale_tx": 1,
                "tx_count_user": 3,
                "rolling_volume_user": 1200000.0,
                "tx_hash": "0x123...",
                "wallet_address": "0xabc..."
            }
        }
    }

class PredictResponse(BaseModel):
    """
    Response schema for risk prediction
    """
    risk_score: float = Field(..., description="Anomaly score (higher = more risky)")
    risk_level: RiskLevel = Field(..., description="Risk classification")
    is_alert: bool = Field(..., description="Whether this triggers an alert")
    threshold: float = Field(..., description="Alert threshold used")
    confidence: float = Field(..., description="Model confidence (0-1)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional blockchain tracking
    alert_tx_hash: Optional[str] = Field(None, description="On-chain alert transaction hash")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_score": 0.85,
                "risk_level": "critical",
                "is_alert": True,
                "threshold": 0.75,
                "confidence": 0.92,
                "timestamp": "2024-02-07T12:00:00",
                "alert_tx_hash": "0xdef..."
            }
        }
    }

class BatchPredictRequest(BaseModel):
    """
    Batch prediction request for multiple transactions
    """
    transactions: List[PredictRequest] = Field(..., max_length=100, description="List of transactions (max 100)")

class BatchPredictResponse(BaseModel):
    """
    Batch prediction response
    """
    predictions: List[PredictResponse]
    total_processed: int
    alerts_triggered: int
    processing_time_ms: float

class AlertRecord(BaseModel):
    """
    Alert record schema for database/blockchain
    """
    id: Optional[int] = None
    tx_hash: Optional[str] = None
    wallet_address: Optional[str] = None
    risk_score: float
    risk_level: RiskLevel
    amount_usd: float
    timestamp: datetime
    on_chain_tx_hash: Optional[str] = None
    verified: bool = False
    false_positive: Optional[bool] = None
    notes: Optional[str] = None

class AlertListResponse(BaseModel):
    """
    Response for listing alerts
    """
    alerts: List[AlertRecord]
    total: int
    page: int
    page_size: int

class SystemStats(BaseModel):
    """
    System statistics
    """
    total_predictions: int
    total_alerts: int
    alert_rate: float
    avg_risk_score: float
    model_version: str
    uptime_seconds: float