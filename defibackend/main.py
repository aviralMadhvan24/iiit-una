"""
DeFi Attack Early Warning System - Backend API
Entry point for the FastAPI application
"""
import asyncio

from app.services.simulator import generate_transaction
from app.services.processor import process_transaction

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.simulator import router as simulator_router


from app.api import predict, alerts, health
from app.auth.wallet import router as wallet_auth_router
from app.api.wallet_activity import router as wallet_activity_router


app = FastAPI(
    title="DeFi Risk Engine",
    description="AI-powered early warning system for DeFi attack detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS (open for hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])
app.include_router(wallet_auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(simulator_router, prefix="/api/v1")


app.include_router(wallet_activity_router, prefix="/api/v1")
