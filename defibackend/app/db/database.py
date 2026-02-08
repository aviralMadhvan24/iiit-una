"""
Database Service
Operational storage for alerts and predictions
NOT used for trust - only operations
"Database is mutable, blockchain is authoritative"
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import List, Optional

from config.settings import settings
from app.schemas.models import (
    PredictRequest,
    PredictResponse,
    AlertRecord,
    RiskLevel,
)

Base = declarative_base()

# ============================
# ORM MODELS
# ============================

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
    false_positive = Column(Boolean, nullable=True)
    notes = Column(String, nullable=True)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, index=True)
    wallet_address = Column(String, index=True)
    amount_usd = Column(Float)
    whale_tx = Column(Integer)
    tx_count_user = Column(Integer)
    rolling_volume_user = Column(Float)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    is_alert = Column(Boolean, default=False)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class TelegramMapping(Base):
    """
    Wallet ↔ Telegram chat mapping
    One wallet = one Telegram chat
    """
    __tablename__ = "telegram_mappings"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True, nullable=False)
    telegram_chat_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================
# DATABASE SERVICE
# ============================

class DatabaseService:
    """
    Database operations service
    Handles all database interactions
    """

    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        print(f"✅ Database initialized at {settings.DATABASE_URL}")

    # ----------------------------
    # PREDICTIONS
    # ----------------------------

    def store_prediction(
        self,
        request: PredictRequest,
        response: PredictResponse,
    ):
        session = self.SessionLocal()
        try:
            prediction = Prediction(
                tx_hash=request.tx_hash,
                wallet_address=request.wallet_address,
                amount_usd=request.amount_usd,
                whale_tx=request.whale_tx,
                tx_count_user=request.tx_count_user,
                rolling_volume_user=request.rolling_volume_user,
                risk_score=response.risk_score,
                risk_level=response.risk_level.value,
                is_alert=response.is_alert,
                confidence=response.confidence,
                timestamp=response.timestamp,
            )
            session.add(prediction)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"❌ Error storing prediction: {e}")
        finally:
            session.close()

    # ----------------------------
    # ALERTS
    # ----------------------------

    def store_alert(
        self,
        request: PredictRequest,
        response: PredictResponse,
        on_chain_tx_hash: Optional[str] = None,
    ) -> int:
        session = self.SessionLocal()
        try:
            alert = Alert(
                tx_hash=request.tx_hash,
                wallet_address=request.wallet_address,
                risk_score=response.risk_score,
                risk_level=response.risk_level.value,
                amount_usd=request.amount_usd,
                timestamp=response.timestamp,
                on_chain_tx_hash=on_chain_tx_hash,
                verified=False,
            )
            session.add(alert)
            session.commit()
            session.refresh(alert)
            return alert.id
        except Exception as e:
            session.rollback()
            print(f"❌ Error storing alert: {e}")
            return -1
        finally:
            session.close()

    def get_alert_by_id(self, alert_id: int) -> Optional[AlertRecord]:
        session = self.SessionLocal()
        try:
            alert = session.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                return None

            return AlertRecord(
                id=alert.id,
                tx_hash=alert.tx_hash,
                wallet_address=alert.wallet_address,
                risk_score=alert.risk_score,
                risk_level=RiskLevel(alert.risk_level),
                amount_usd=alert.amount_usd,
                timestamp=alert.timestamp,
                on_chain_tx_hash=alert.on_chain_tx_hash,
                verified=alert.verified,
                false_positive=alert.false_positive,
                notes=alert.notes,
            )
        finally:
            session.close()

    def get_alerts(
        self,
        skip: int = 0,
        limit: int = 100,
        wallet_address: Optional[str] = None,
        risk_level: Optional[RiskLevel] = None,
    ) -> List[AlertRecord]:
        session = self.SessionLocal()
        try:
            query = session.query(Alert)

            if wallet_address:
                query = query.filter(Alert.wallet_address == wallet_address)

            if risk_level:
                query = query.filter(Alert.risk_level == risk_level.value)

            alerts = (
                query.order_by(Alert.timestamp.desc())
                .offset(skip)
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
                    false_positive=a.false_positive,
                    notes=a.notes,
                )
                for a in alerts
            ]
        finally:
            session.close()

    # ----------------------------
    # TELEGRAM MAPPING
    # ----------------------------

    def save_telegram_chat_id(
        self,
        wallet_address: str,
        telegram_chat_id: str,
    ):
        session = self.SessionLocal()
        try:
            mapping = (
                session.query(TelegramMapping)
                .filter(TelegramMapping.wallet_address == wallet_address)
                .first()
            )

            if mapping:
                mapping.telegram_chat_id = telegram_chat_id
            else:
                mapping = TelegramMapping(
                    wallet_address=wallet_address,
                    telegram_chat_id=telegram_chat_id,
                )
                session.add(mapping)

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"❌ Error saving Telegram mapping: {e}")
        finally:
            session.close()

    def get_telegram_chat_id(
        self,
        wallet_address: str,
    ) -> Optional[str]:
        session = self.SessionLocal()
        try:
            mapping = (
                session.query(TelegramMapping.telegram_chat_id)
                .filter(TelegramMapping.wallet_address == wallet_address)
                .first()
            )
            return mapping[0] if mapping else None
        finally:
            session.close()

    # ----------------------------
    # STATS
    # ----------------------------

    def get_statistics(self) -> dict:
        session = self.SessionLocal()
        try:
            total_predictions = session.query(Prediction).count()
            total_alerts = session.query(Alert).count()

            alert_rate = (
                total_alerts / total_predictions
                if total_predictions > 0
                else 0.0
            )

            avg_risk = session.query(Prediction.risk_score).all()
            avg_risk_score = (
                sum(r[0] for r in avg_risk) / len(avg_risk)
                if avg_risk
                else 0.0
            )

            return {
                "total_predictions": total_predictions,
                "total_alerts": total_alerts,
                "alert_rate": alert_rate,
                "avg_risk_score": avg_risk_score,
            }
        finally:
            session.close()
