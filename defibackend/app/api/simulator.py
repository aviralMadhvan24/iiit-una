from fastapi import APIRouter
from app.services.simulator_controller import (
    start_simulator,
    stop_simulator,
    simulator_status,
)
from app.db.database import DatabaseService

router = APIRouter(prefix="/simulator", tags=["Simulator"])
db = DatabaseService()


@router.post("/start")
async def start():
    started = await start_simulator()
    return {
        "running": simulator_status(),
        "message": "Simulator started" if started else "Already running",
    }


@router.post("/stop")
async def stop():
    stopped = await stop_simulator()
    return {
        "running": simulator_status(),
        "message": "Simulator stopped" if stopped else "Already stopped",
    }


@router.post("/reset")
async def reset():
    """
    Reset all simulated transactions and alerts.
    Simulator must be stopped first (recommended).
    """
    if simulator_status():
        await stop_simulator()

    db.reset_transactions()

    return {
        "running": False,
        "message": "Transactions reset successfully",
    }


@router.get("/status")
async def status():
    return {"running": simulator_status()}
