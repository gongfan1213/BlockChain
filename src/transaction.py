"""
Transaction Module

Implements single-input single-output (SISO) transactions with cryptographic validation.

This module provides core functionality for:
- Creating and signing transactions
- Validating transaction signatures
- Generating unique transaction IDs
"""
from hashlib import sha256
from typing import Tuple
from dataclasses import dataclass
from .accounts import BlockchainAccount

@dataclass
class Transaction:
    """
    Represents a blockchain transaction with sender, receiver, amount and signature.

    Attributes:
        sender (str): Sender's blockchain address
        receiver (str): Receiver's blockchain address
        amount (int): Transaction amount
        signature (bytes): Digital signature of the transaction
    """
    sender: str
    receiver: str
    amount: int
    signature: bytes
    
    @property
    def txid(self) -> str:
        """
        Generate transaction ID using SHA-256 hash of transaction contents.

        Returns:
            str: Unique transaction identifier (64-character hex string)
        """
        data = f"{self.sender}{self.receiver}{self.amount}".encode()
        return sha256(data).hexdigest()

    def validate(self) -> bool:
        """
        Verify transaction signature using sender's public key.

        Returns:
            bool: True if signature is valid, False otherwise
        """
        return BlockchainAccount.verify_signature(
            self.sender,
            self.signature,
            f"{self.amount}".encode()
        )

    @classmethod
    def create_transaction(cls, sender: BlockchainAccount, receiver_address: str, amount: int):
        """
        Factory method to create properly signed transactions.

        Args:
            sender (BlockchainAccount): Sender's account object
            receiver_address (str): Receiver's blockchain address
            amount (int): Transaction amount

        Returns:
            Transaction: Newly created and signed transaction
        """
        signature = sender.sign_transaction(f"{amount}".encode())
        return cls(
            sender=sender.address,
            receiver=receiver_address,
            amount=amount,
            signature=signature
        )