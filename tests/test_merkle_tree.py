import pytest
from src.merkle_tree import MerkleTree
from src.transaction import Transaction
from src.account import Account

def test_merkle_tree_creation():
    transactions = []
    for _ in range(4):
        sender = Account()
        receiver = Account()
        tx = Transaction(sender.get_address(), receiver.get_address(), 100)
        tx.sign_transaction(sender)
        transactions.append(tx)
    
    tree = MerkleTree(transactions)
    root_hash = tree.build()
    assert root_hash is not None
    assert isinstance(root_hash, str)
    assert len(root_hash) == 64

def test_merkle_tree_verification():
    transactions = []
    for _ in range(4):
        sender = Account()
        receiver = Account()
        tx = Transaction(sender.get_address(), receiver.get_address(), 100)
        tx.sign_transaction(sender)
        transactions.append(tx)
    
    tree = MerkleTree(transactions)
    tree.build()
    
    # 验证所有交易
    for tx in transactions:
        assert tree.verify_transaction(tx)

def test_merkle_tree_tampering():
    transactions = []
    for _ in range(4):
        sender = Account()
        receiver = Account()
        tx = Transaction(sender.get_address(), receiver.get_address(), 100)
        tx.sign_transaction(sender)
        transactions.append(tx)
    
    tree = MerkleTree(transactions)
    tree.build()
    
    # 篡改交易
    tampered_tx = transactions[0]
    tampered_tx.amount = 200
    
    assert not tree.verify_transaction(tampered_tx)

def test_empty_tree():
    with pytest.raises(ValueError):
        tree = MerkleTree([])
        tree.build()