"""
DeFi Attack Early Warning System - Backend API
Entry point for the FastAPI application
"""
import asyncio

from app.services.simulator import generate_transaction
from app.services.alert_engine import process_transaction

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import predict, alerts, health
from app.auth.wallet import router as wallet_auth_router

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

@app.on_event("startup")
async def startup_event():
    print("🚀 DeFi Risk Engine starting up...")
    print("📊 Model version: v1.0")
    print("🔗 Blockchain network: sepolia")
    print("⚙️ Starting simulated transaction pool...")
    print("✅ Ready to detect attacks!")

    async def simulator_loop():
        while True:
            tx = generate_transaction()
            process_transaction(tx)
            await asyncio.sleep(3)  # one tx every 3 seconds

    asyncio.create_task(simulator_loop())
