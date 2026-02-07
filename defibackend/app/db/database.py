from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Optional

from app.schemas.models import AlertRecord, RiskLevel

DATABASE_URL = "sqlite:///./alerts.db"

Base = declarative_base()


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, index=True)
    wallet_address = Column(String, index=True)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    amount_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    on_chain_tx_hash = Column(String, nullable=True)
    verified = Column(Boolean, default=False)


class DatabaseService:
    """
    SQLite-backed operational database (hackathon-safe)
    """

    def __init__(self):
        self.engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def store_alert(
        self,
        tx_hash: str,
        wallet_address: str,
        risk_score: float,
        risk_level: RiskLevel,
        amount_usd: float,
        on_chain_tx_hash: Optional[str] = None,
    ):
        session = self.SessionLocal()
        try:
            alert = Alert(
                tx_hash=tx_hash,
                wallet_address=wallet_address,
                risk_score=risk_score,
                risk_level=risk_level.value,
                amount_usd=amount_usd,
                on_chain_tx_hash=on_chain_tx_hash,
            )
            session.add(alert)
            session.commit()
        finally:
            session.close()

    def get_alerts(self, limit: int = 50) -> List[AlertRecord]:
        session = self.SessionLocal()
        try:
            alerts = (
                session.query(Alert)
                .order_by(Alert.timestamp.desc())
                .limit(limit)
                .all()
            )
            return [
                AlertRecord(
                    id=a.id,
                    tx_hash=a.tx_hash,
                    wallet_address=a.wallet_address,
                    risk_score=a.risk_score,
                    risk_level=RiskLevel(a.risk_level),
                    amount_usd=a.amount_usd,
                    timestamp=a.timestamp,
                    on_chain_tx_hash=a.on_chain_tx_hash,
                    verified=a.verified,
                )
                for a in alerts
            ]
        finally:
            session.close()
