"""
DeFi Attack Early Warning System - Backend API
Entry point for the FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict, alerts, health

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

@app.on_event("startup")
async def startup_event():
    print("🚀 DeFi Risk Engine starting up...")
    print("📊 Model version: v1.0")
    print("🔗 Blockchain network: sepolia")
    print("✅ Ready to detect attacks!")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 DeFi Risk Engine shutting down...")
