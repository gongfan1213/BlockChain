import pytest
from src.blockchain import Blockchain, Block
from src.transaction import Transaction
from src.account import Account
from src.verification import BlockchainVerifier

def test_blockchain_integrity():
    blockchain = Blockchain(difficulty=3)
    accounts = [Account() for _ in range(3)]
    
    # 创建并添加多个交易
    transactions = []
    for i in range(2):
        tx = Transaction(accounts[i].get_address(), accounts[i+1].get_address(), 100)
        tx.sign_transaction(accounts[i])
        transactions.append(tx)
        blockchain.add_transaction(tx)
    
    block = blockchain.mine_pending_transactions(accounts[-1].get_address())
    verifier = BlockchainVerifier()
    
    # 基本完整性检查
    assert verifier.verify_chain(blockchain)
    
    # 测试各种篡改情况
    def test_tamper_scenarios():
        # 1. 修改交易金额
        tampered_tx = transactions[0]
        tampered_tx.amount = 200
        tampering_info = verifier.detect_tampering(
            blockchain.chain[1],
            Block([tampered_tx] + transactions[1:], blockchain.chain[0].hash)
        )
        assert tampering_info['is_tampered']
        
        # 2. 修改时间戳
        tampered_block = Block(transactions, blockchain.chain[0].hash)
        tampered_block.timestamp += 1000
        tampering_info = verifier.detect_tampering(blockchain.chain[1], tampered_block)
        assert tampering_info['is_tampered']
        
        # 3. 修改前一个哈希
        tampered_block = Block(transactions, "fake_hash")
        tampering_info = verifier.detect_tampering(blockchain.chain[1], tampered_block)
        assert tampering_info['is_tampered']
    
    test_tamper_scenarios()

def test_chain_validation():
    blockchain = Blockchain(difficulty=2)
    verifier = BlockchainVerifier()
    
    # 测试创世区块
    assert verifier.verify_chain(blockchain)
    
    # 添加新区块
    sender = Account()
    receiver = Account()
    tx = Transaction(sender.get_address(), receiver.get_address(), 100)
    tx.sign_transaction(sender)
    blockchain.add_transaction(tx)
    blockchain.mine_pending_transactions(receiver.get_address())
    
    assert verifier.verify_chain(blockchain)