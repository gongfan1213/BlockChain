from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import hashlib
import json
from datetime import datetime
#- cryptography : 用于密码学操作
#- hashlib : 用于SHA-256哈希计算
#- pytest : 用于单元测试
#- datetime : 用于时间戳
# 交易生成模块
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now().timestamp()
        self.signature = None
        self.transaction_id = None
        
    def calculate_hash(self):
        """计算交易的哈希值"""
        transaction_dict = {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        transaction_str = json.dumps(transaction_dict, sort_keys=True)
        return hashlib.sha256(transaction_str.encode()).hexdigest()
    
    def sign_transaction(self, private_key):
        """使用私钥签名交易"""
        transaction_hash = self.calculate_hash().encode()
        self.signature = private_key.sign(
            transaction_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.transaction_id = self.calculate_hash()