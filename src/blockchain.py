from datetime import datetime
import hashlib
import json
from .merkle_tree import MerkleTree

class Block:
    def __init__(self, transactions, previous_hash, difficulty=4):
        self.timestamp = datetime.now().timestamp()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.merkle_tree = MerkleTree(transactions)
        self.merkle_root = self.merkle_tree.build()
        self.hash = self.calculate_hash()
        
    def to_dict(self):
        """将区块转换为字典格式"""
        return {
            'timestamp': self.timestamp,
            'transactions': [tx.transaction_id for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'merkle_root': self.merkle_root
        }
        
    def calculate_hash(self):
        """计算区块哈希"""
        block_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()
        
    def mine_block(self):
        """挖矿实现"""
        target = '0' * self.difficulty
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return True

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = Block([], "0", self.difficulty)
        self.chain.append(genesis_block)
        
    def get_latest_block(self):
        """获取最新区块"""
        return self.chain[-1]
        
    def add_transaction(self, transaction):
        """添加交易到待处理列表"""
        self.pending_transactions.append(transaction)
        
    def mine_pending_transactions(self, miner_address):
        """挖掘待处理的交易"""
        block = Block(self.pending_transactions, self.get_latest_block().hash, self.difficulty)
        block.mine_block()
        
        self.chain.append(block)
        self.pending_transactions = []
        
        return block