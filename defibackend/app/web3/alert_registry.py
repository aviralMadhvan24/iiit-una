"""
Alert Registry
Manages on-chain alert creation
Blockchain used for AUDITABILITY, not computation
"""

from typing import Optional
from web3 import Web3
from app.web3.client import Web3Client
from config.settings import settings


# ✅ ABI MUST MATCH DEPLOYED CONTRACT EXACTLY
# Solidity:
# function createAlert(bytes32 _txHash, uint8 _riskScore) external
ALERT_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_txHash", "type": "bytes32"},
            {"internalType": "uint8", "name": "_riskScore", "type": "uint8"}
        ],
        "name": "createAlert",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


class AlertRegistry:
    """
    On-chain alert registry
    Purpose: Immutable audit trail, not real-time computation
    """

    def __init__(self):
        self.web3_client = Web3Client()
        self.contract = None
        self._initialize_contract()

    def _initialize_contract(self):
        """
        Initialize smart contract instance
        """
        if not self.web3_client.is_connected():
            print("⚠️ Web3 not connected - alerts will be DB-only")
            return

        contract_address = settings.ALERT_REGISTRY_CONTRACT

        if not contract_address or contract_address == "0x...":
            print("ℹ️ Alert registry contract not configured")
            return

        try:
            self.contract = self.web3_client.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=ALERT_REGISTRY_ABI
            )
            print(f"✅ Alert registry contract loaded at {contract_address}")
        except Exception as e:
            print(f"⚠️ Contract initialization error: {e}")
            self.contract = None

    async def create_alert(
        self,
        wallet_address: str,  # kept for API consistency (NOT used on-chain)
        risk_score: float,
        tx_hash: str
    ) -> Optional[str]:
        """
        Create alert on-chain

        Args:
            wallet_address: ignored by contract (off-chain metadata only)
            risk_score: float (0–1)
            tx_hash: transaction hash string

        Returns:
            blockchain tx hash or None
        """

        if not self.contract or not self.web3_client.is_connected():
            print("ℹ️ Blockchain unavailable - alert stored in DB only")
            return None

        try:
            # 🔐 tx_hash → bytes32
            tx_hash_bytes32 = Web3.keccak(text=tx_hash)

            # 🔢 risk_score → uint8 (0–255)
            risk_score_uint8 = min(int(risk_score * 100), 255)

            account_address = self.web3_client.get_account()
            if not account_address:
                print("⚠️ No signing account configured")
                return None

            # ✅ EXACTLY TWO ARGUMENTS — MATCHES ABI
            transaction = self.contract.functions.createAlert(
                tx_hash_bytes32,
                risk_score_uint8
            ).build_transaction({
                "from": account_address,
                "nonce": self.web3_client.w3.eth.get_transaction_count(account_address),
                "gas": 150000,
                "gasPrice": self.web3_client.w3.eth.gas_price
            })

            signed_txn = self.web3_client.w3.eth.account.sign_transaction(
                transaction,
                private_key=settings.PRIVATE_KEY
            )

            tx_hash_result = self.web3_client.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )

            print(f"✅ Alert created on-chain: {tx_hash_result.hex()}")
            return tx_hash_result.hex()

        except Exception as e:
            print(f"⚠️ On-chain alert creation failed: {e}")
            print("ℹ️ Alert will be stored in database only")
            return None

    def is_available(self) -> bool:
        """Check if on-chain registry is available"""
        return self.contract is not None and self.web3_client.is_connected()
