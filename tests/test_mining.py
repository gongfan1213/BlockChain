import pytest
from src.blockchain import Blockchain, Block
from src.transaction import Transaction
from src.account import Account
import time

def test_mining_block():
    # 创建区块链
    blockchain = Blockchain(difficulty=4)
    
    # 创建测试账户
    sender = Account()
    receiver = Account()
    
    # 创建测试交易
    tx = Transaction(sender.get_address(), receiver.get_address(), 100)
    tx.sign_transaction(sender)
    
    # 添加交易并挖矿
    blockchain.add_transaction(tx)
    start_time = time.time()
    block = blockchain.mine_pending_transactions(receiver.get_address())
    end_time = time.time()
    
    # 验证
    assert block.hash.startswith('0' * blockchain.difficulty)
    assert len(blockchain.chain) == 2  # 创世区块 + 新区块
    assert len(blockchain.pending_transactions) == 0
    
    # 输出挖矿性能数据
    print(f"Mining time: {end_time - start_time:.2f} seconds")
    print(f"Final nonce: {block.nonce}")