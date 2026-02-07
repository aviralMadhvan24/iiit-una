from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.predict import router as predict_router
from app.api.alerts import router as alerts_router
from app.auth.wallet import router as wallet_auth_router

router = APIRouter()

router.include_router(health_router)
router.include_router(predict_router)
router.include_router(alerts_router)
router.include_router(wallet_auth_router)
