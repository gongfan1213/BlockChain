"""
Blockchain Account Management Module

Implements ECC-based key generation and address derivation using NIST P-256 curve.

This module provides core functionality for:
- Generating cryptographic key pairs
- Deriving blockchain addresses
- Signing and verifying transactions
"""
from ecdsa import SigningKey, NIST256p

class BlockchainAccount:
    def __init__(self):
        """
        Initialize a new blockchain account.

        Generates a new ECC key pair using NIST P-256 curve:
        - private_key: Used for signing transactions
        - public_key: Used for verification and address derivation
        """
        self.private_key = SigningKey.generate(curve=NIST256p)
        self.public_key = self.private_key.get_verifying_key()

    @property
    def address(self):
        """
        Generate the blockchain address from public key.

        Returns:
            str: Hex representation of the public key (128 characters)
        """
        return self.public_key.to_string().hex()

    def sign_transaction(self, transaction_data: bytes) -> bytes:
        """
        Sign transaction data using the account's private key.

        Args:
            transaction_data (bytes): The data to be signed

        Returns:
            bytes: Digital signature of the transaction data
        """
        return self.private_key.sign(transaction_data)

    @staticmethod
    def verify_signature(public_key_hex: str, signature: bytes, data: bytes) -> bool:
        """
        Verify the authenticity of a signature using the sender's public key.

        Args:
            public_key_hex (str): Sender's public key in hex format
            signature (bytes): The signature to verify
            data (bytes): The original signed data

        Returns:
            bool: True if signature is valid, False otherwise

        Note:
            Creates verifying key directly from hex string for verification
        """
        try:
            from ecdsa import VerifyingKey
            vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=NIST256p)
            return vk.verify(signature, data)
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")
            return False