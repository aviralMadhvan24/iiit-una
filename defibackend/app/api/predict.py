"""
Prediction API Routes
ONLY HTTP logic - no ML here
Orchestrates calls to inference and scoring services
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
import time

from app.schemas.models import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResponse,
    RiskLevel,
)
from app.services.inference import InferenceService
from app.services.scoring import ScoringService
from app.db.database import DatabaseService
from app.web3.alert_registry import AlertRegistry

# 🔔 Telegram notification service
from app.notifications.telegram_service import notify_telegram

router = APIRouter()

# ============================
# SERVICE INITIALIZATION
# ============================

inference_service = InferenceService()
scoring_service = ScoringService()
db_service = DatabaseService()
alert_registry = AlertRegistry()


# ============================
# SINGLE PREDICTION
# ============================

@router.post("/predict", response_model=PredictResponse)
async def predict_transaction(
    request: PredictRequest,
    background_tasks: BackgroundTasks,
):
    """
    Predict risk score for a single transaction
    """
    try:
        # ================== 1. ML INFERENCE ==================
        risk_score = inference_service.run_inference(request)

        # ================== 2. SCORING ==================
        risk_level = scoring_service.classify_risk_level(risk_score)
        is_alert = scoring_service.should_alert(risk_score)
        confidence = scoring_service.calculate_confidence(risk_score)
        threshold = scoring_service.threshold

        response = PredictResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            is_alert=is_alert,
            threshold=threshold,
            confidence=confidence,
            timestamp=datetime.utcnow(),
        )

        # ================== 3. STORE PREDICTION ==================
        background_tasks.add_task(
            db_service.store_prediction,
            request=request,
            response=response,
        )

        # ================== 4. STORE ALERT (DB FIRST) ==================
        if is_alert:
            alert_id = db_service.store_alert(
                request=request,
                response=response,
                on_chain_tx_hash=None,
            )

            # ================== 5. TELEGRAM NOTIFICATION ==================
            chat_id = db_service.get_telegram_chat_id(
                request.wallet_address
            )

            if chat_id and alert_id != -1:
                alert_record = db_service.get_alert_by_id(alert_id)
                if alert_record:
                    background_tasks.add_task(
                        notify_telegram,
                        chat_id,
                        alert_record,
                    )

        # ================== 6. ON-CHAIN ALERT ==================
        if is_alert and risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            background_tasks.add_task(
                alert_registry.create_alert,
                wallet_address=request.wallet_address or "unknown",
                risk_score=risk_score,
                tx_hash=request.tx_hash or "unknown",
            )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )


# ============================
# BATCH PREDICTION
# ============================

@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(
    request: BatchPredictRequest,
    background_tasks: BackgroundTasks,
):
    """
    Batch prediction for multiple transactions
    """
    start_time = time.time()

    try:
        risk_scores = inference_service.batch_inference(
            request.transactions
        )

        predictions = []
        alerts_triggered = 0

        for tx, risk_score in zip(
            request.transactions, risk_scores
        ):
            risk_level = scoring_service.classify_risk_level(risk_score)
            is_alert = scoring_service.should_alert(risk_score)
            confidence = scoring_service.calculate_confidence(risk_score)

            if is_alert:
                alerts_triggered += 1

            prediction = PredictResponse(
                risk_score=risk_score,
                risk_level=risk_level,
                is_alert=is_alert,
                threshold=scoring_service.threshold,
                confidence=confidence,
                timestamp=datetime.utcnow(),
            )

            predictions.append(prediction)

            # Store prediction
            background_tasks.add_task(
                db_service.store_prediction,
                request=tx,
                response=prediction,
            )

            # Store alert ONLY (no Telegram in batch to avoid spam)
            if is_alert:
                background_tasks.add_task(
                    db_service.store_alert,
                    request=tx,
                    response=prediction,
                    on_chain_tx_hash=None,
                )

        processing_time_ms = (
            time.time() - start_time
        ) * 1000

        return BatchPredictResponse(
            predictions=predictions,
            total_processed=len(predictions),
            alerts_triggered=alerts_triggered,
            processing_time_ms=processing_time_ms,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}",
        )
