"""
Blockchain Account Management Module
Implements ECC-based key generation and address derivation
"""
from ecdsa import SigningKey, NIST256p

class BlockchainAccount:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=NIST256p)
        self.public_key = self.private_key.get_verifying_key()

    @property
    def address(self):
        return self.public_key.to_string().hex()

    def sign_transaction(self, transaction_data: bytes) -> bytes:
        return self.private_key.sign(transaction_data)

    @staticmethod
    def verify_signature(public_key_hex: str, signature: bytes, data: bytes) -> bool:
        try:
            # 直接从十六进制字符串创建验证密钥，而不是从签名密钥创建
            from ecdsa import VerifyingKey
            vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=NIST256p)
            return vk.verify(signature, data)
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")
            return False