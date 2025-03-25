"""
Transaction Module
Implements single-input single-output (SISO) transactions with cryptographic validation
"""
from hashlib import sha256
from typing import Tuple
from dataclasses import dataclass
from .accounts import BlockchainAccount

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: int
    signature: bytes
    
    @property
    def txid(self) -> str:
        """Generate transaction ID using SHA-256 hash of transaction contents"""
        data = f"{self.sender}{self.receiver}{self.amount}".encode()
        return sha256(data).hexdigest()

    def validate(self) -> bool:
        """Verify transaction signature using sender's public key"""
        return BlockchainAccount.verify_signature(
            self.sender,
            self.signature,
            f"{self.amount}".encode()
        )

    @classmethod
    def create_transaction(cls, sender: BlockchainAccount, receiver_address: str, amount: int):
        """Factory method to create properly signed transactions"""
        signature = sender.sign_transaction(f"{amount}".encode())
        return cls(
            sender=sender.address,
            receiver=receiver_address,
            amount=amount,
            signature=signature
        )