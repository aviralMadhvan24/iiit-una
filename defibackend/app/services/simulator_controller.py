import asyncio
from typing import Optional

from app.services.simulator import generate_transaction
from app.services.processor import process_transaction

_simulator_task: Optional[asyncio.Task] = None
_running: bool = False


async def _simulator_loop():
    print("▶️ Simulator started")
    try:
        while _running:
            tx = generate_transaction()
            process_transaction(tx)
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        print("⏹️ Simulator stopped")


def simulator_status() -> bool:
    return _running


async def start_simulator() -> bool:
    global _simulator_task, _running

    if _running:
        return False

    _running = True
    _simulator_task = asyncio.create_task(_simulator_loop())
    return True


async def stop_simulator() -> bool:
    global _simulator_task, _running

    if not _running:
        return False

    _running = False

    if _simulator_task:
        _simulator_task.cancel()
        _simulator_task = None

    return True
