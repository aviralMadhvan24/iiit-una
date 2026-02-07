from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from eth_account.messages import encode_defunct
from web3 import Web3
import secrets
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

JWT_SECRET = "CHANGE_ME"
JWT_ALGO = "HS256"

NONCES = {}

class VerifyRequest(BaseModel):
    wallet: str
    signature: str


@router.get("/nonce/{wallet}")
def get_nonce(wallet: str):
    nonce = secrets.token_hex(16)
    NONCES[wallet.lower()] = nonce
    return {"nonce": nonce}


@router.post("/verify")
def verify(payload: VerifyRequest):
    wallet = payload.wallet.lower()
    signature = payload.signature

    if wallet not in NONCES:
        raise HTTPException(status_code=400, detail="Nonce not found")

    message = f"Login to DeFi Sentinel\nNonce: {NONCES[wallet]}"
    encoded = encode_defunct(text=message)

    recovered = Web3().eth.account.recover_message(
        encoded,
        signature=signature
    ).lower()

    if recovered != wallet:
        raise HTTPException(status_code=401, detail="Invalid signature")

    token = jwt.encode(
        {
            "wallet": wallet,
            "exp": datetime.utcnow() + timedelta(hours=12),
        },
        JWT_SECRET,
        algorithm=JWT_ALGO,
    )

    del NONCES[wallet]
    return {"access_token": token}
