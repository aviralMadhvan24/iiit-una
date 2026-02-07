"""
DeFi Attack Early Warning System - Backend API
Entry point for the FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict, alerts, health
from config.settings import settings

# Initialize FastAPI app
app = FastAPI(
    title="DeFi Risk Engine",
    description="AI-powered early warning system for DeFi attack detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - clean separation of concerns
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 DeFi Risk Engine starting up...")
    print(f"📊 Model version: {settings.MODEL_VERSION}")
    print(f"🔗 Blockchain network: {settings.WEB3_NETWORK}")
    print("✅ Ready to detect attacks!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 DeFi Risk Engine shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )