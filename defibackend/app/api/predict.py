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
    RiskLevel
)
from app.services.inference import InferenceService
from app.services.scoring import ScoringService
from app.db.database import DatabaseService
from app.web3.alert_registry import AlertRegistry

router = APIRouter()

# Initialize services
inference_service = InferenceService()
scoring_service = ScoringService()
db_service = DatabaseService()
alert_registry = AlertRegistry()

@router.post("/predict", response_model=PredictResponse)
async def predict_transaction(
    request: PredictRequest,
    background_tasks: BackgroundTasks
):
    """
    Predict risk score for a single transaction
    
    Flow:
    1. Validate input (handled by Pydantic)
    2. Run ML inference
    3. Apply scoring logic
    4. Store result in DB
    5. Create on-chain alert if needed (background)
    """
    try:
        # Step 1: Get raw risk score from ML model
        risk_score = inference_service.run_inference(request)
        
        # Step 2: Apply decision logic
        risk_level = scoring_service.classify_risk_level(risk_score)
        is_alert = scoring_service.should_alert(risk_score)
        confidence = scoring_service.calculate_confidence(risk_score)
        threshold = scoring_service.threshold
        
        # Step 3: Prepare response
        response = PredictResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            is_alert=is_alert,
            threshold=threshold,
            confidence=confidence,
            timestamp=datetime.utcnow()
        )
        
        # Step 4: Store in database (async)
        background_tasks.add_task(
            db_service.store_prediction,
            request=request,
            response=response
        )
        
        # Step 5: Create on-chain alert if critical (async)
        if is_alert and risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            background_tasks.add_task(
                alert_registry.create_alert,
                wallet_address=request.wallet_address or "unknown",
                risk_score=risk_score,
                tx_hash=request.tx_hash or "unknown"
            )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(
    request: BatchPredictRequest,
    background_tasks: BackgroundTasks
):
    """
    Batch prediction for multiple transactions
    More efficient than individual calls
    """
    start_time = time.time()
    
    try:
        # Step 1: Batch inference
        risk_scores = inference_service.batch_inference(request.transactions)
        
        # Step 2: Process each result
        predictions = []
        alerts_triggered = 0
        
        for i, (tx, risk_score) in enumerate(zip(request.transactions, risk_scores)):
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
                timestamp=datetime.utcnow()
            )
            predictions.append(prediction)
            
            # Store in background
            background_tasks.add_task(
                db_service.store_prediction,
                request=tx,
                response=prediction
            )
        
        # Step 3: Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        return BatchPredictResponse(
            predictions=predictions,
            total_processed=len(predictions),
            alerts_triggered=alerts_triggered,
            processing_time_ms=processing_time_ms
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@router.get("/predict/threshold")
async def get_threshold():
    """
    Get current alert threshold configuration
    """
    return scoring_service.get_threshold_info()

@router.post("/predict/threshold")
async def update_threshold(new_threshold: float):
    """
    Update alert threshold
    Useful for protocol-specific tuning
    """
    try:
        scoring_service.update_threshold(new_threshold)
        return {
            "message": "Threshold updated successfully",
            "new_threshold": new_threshold
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/predict/model-info")
async def get_model_info():
    """
    Get information about the loaded model
    """
    model_loader = inference_service.model_loader
    return model_loader.get_model_info()