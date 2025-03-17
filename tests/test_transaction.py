import pytest
from src.transaction import Transaction
from src.account import Account
import time

def test_transaction_creation():
    sender = Account()
    receiver = Account()
    amount = 100
    tx = Transaction(sender.get_address(), receiver.get_address(), amount)
    
    assert tx.sender_address == sender.get_address()
    assert tx.receiver_address == receiver.get_address()
    assert tx.amount == amount
    assert tx.timestamp is not None

def test_transaction_signing():
    sender = Account()
    receiver = Account()
    tx = Transaction(sender.get_address(), receiver.get_address(), 100)
    tx.sign_transaction(sender)
    
    assert tx.signature is not None
    assert tx.transaction_id is not None

def test_transaction_hash_uniqueness():
    sender = Account()
    receiver = Account()
    tx1 = Transaction(sender.get_address(), receiver.get_address(), 100)
    time.sleep(0.1)  # 确保时间戳不同
    tx2 = Transaction(sender.get_address(), receiver.get_address(), 100)
    
    assert tx1.calculate_hash() != tx2.calculate_hash()

def test_invalid_amount():
    with pytest.raises(ValueError):
        sender = Account()
        receiver = Account()
        Transaction(sender.get_address(), receiver.get_address(), -100)