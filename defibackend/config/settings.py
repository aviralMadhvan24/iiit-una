"""
Configuration settings for DeFi Risk Engine
Centralized configuration management
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DeFi Risk Engine"
    DEBUG: bool = False
    MODEL_VERSION: str = "v1.0"
    
    # API
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Model paths
    MODEL_PATH: str = "models/isolation_forest.pkl"
    SCALER_PATH: str = "models/scaler.pkl"
    
    # Risk thresholds
    RISK_THRESHOLD_PERCENTILE: float = 98.0  # Top 2% are flagged
    HIGH_RISK_THRESHOLD: float = 0.7  # Above this = critical alert
    
    # Web3
    WEB3_NETWORK: str = "sepolia"  # testnet for demo
    WEB3_RPC_URL: str = "https://eth-sepolia.g.alchemy.com/v2/demo"
    ALERT_REGISTRY_CONTRACT: str = "0x..."  # Contract address
    PRIVATE_KEY: str = ""  # Set via environment variable
    
    # Database
    DATABASE_URL: str = "sqlite:///./defi_risk.db"
    
    # Feature names (must match training)
    FEATURE_NAMES: List[str] = [
        "amount_usd",
        "whale_tx",
        "tx_count_user",
        "rolling_volume_user"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()