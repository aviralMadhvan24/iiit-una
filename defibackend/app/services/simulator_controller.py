# app/services/simulator_controller.py

import asyncio
from app.services.simulator import generate_transaction
from app.services.processor import process_transaction

_running = False

async def simulator_loop():
    print("▶️ Simulator background loop started")
    while True:
        if _running:
            tx = generate_transaction()
            process_transaction(tx)
        await asyncio.sleep(3)

def simulator_status() -> bool:
    return _running

def start_simulator() -> bool:
    global _running
    if _running:
        return False
    _running = True
    print("▶️ Simulator ON")
    return True

def stop_simulator() -> bool:
    global _running
    if not _running:
        return False
    _running = False
    print("⏹️ Simulator OFF")
    return True
