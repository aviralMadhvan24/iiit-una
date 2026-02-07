"""
Web3 Client
Handles blockchain connections
ISOLATED: If Web3 fails, backend still works
"""
from web3 import Web3
from typing import Optional
from config.settings import settings

class Web3Client:
    """
    Web3 connection manager
    Isolated from core business logic
    """
    
    def __init__(self):
        self.w3: Optional[Web3] = None
        self._connect()
    
    def _connect(self):
        """
        Establish Web3 connection
        Fails gracefully if RPC unavailable
        """
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL))
            
            if self.w3.is_connected():
                print(f"✅ Connected to {settings.WEB3_NETWORK}")
                print(f"📍 Block number: {self.w3.eth.block_number}")
            else:
                print("⚠️ Web3 connection failed - running in degraded mode")
                self.w3 = None
                
        except Exception as e:
            print(f"⚠️ Web3 initialization error: {e}")
            self.w3 = None
    
    def is_connected(self) -> bool:
        """Check if Web3 is connected"""
        return self.w3 is not None and self.w3.is_connected()
    
    def get_block_number(self) -> Optional[int]:
        """Get current block number"""
        if not self.is_connected():
            return None
        try:
            return self.w3.eth.block_number
        except Exception as e:
            print(f"Error getting block number: {e}")
            return None
    
    def get_transaction(self, tx_hash: str) -> Optional[dict]:
        """
        Get transaction details
        Args:
            tx_hash: transaction hash
        Returns:
            transaction dict or None
        """
        if not self.is_connected():
            return None
        
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            return dict(tx)
        except Exception as e:
            print(f"Error fetching transaction {tx_hash}: {e}")
            return None
    
    def get_account(self) -> Optional[str]:
        """
        Get account from private key
        Returns:
            account address or None
        """
        if not settings.PRIVATE_KEY:
            return None
        
        try:
            account = self.w3.eth.account.from_key(settings.PRIVATE_KEY)
            return account.address
        except Exception as e:
            print(f"Error loading account: {e}")
            return None
    
    def get_balance(self, address: str) -> Optional[float]:
        """
        Get ETH balance of address
        Args:
            address: wallet address
        Returns:
            balance in ETH or None
        """
        if not self.is_connected():
            return None
        
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            print(f"Error getting balance for {address}: {e}")
            return None
    
    def estimate_gas(self, transaction: dict) -> Optional[int]:
        """
        Estimate gas for transaction
        Args:
            transaction: transaction dict
        Returns:
            estimated gas or None
        """
        if not self.is_connected():
            return None
        
        try:
            gas = self.w3.eth.estimate_gas(transaction)
            return gas
        except Exception as e:
            print(f"Error estimating gas: {e}")
            return None