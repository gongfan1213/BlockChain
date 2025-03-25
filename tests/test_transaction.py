"""
Transaction Module Tests
Verifies SISO transaction creation and validation
"""
import pytest
from src.accounts import BlockchainAccount
from src.transaction import Transaction

@pytest.fixture
def sample_transaction():
    sender = BlockchainAccount()
    receiver = BlockchainAccount()
    return Transaction.create_transaction(sender, receiver.address, 100)

def test_transaction_creation(sample_transaction):
    assert len(sample_transaction.txid) == 64
    assert sample_transaction.sender == sample_transaction.sender
    assert sample_transaction.receiver
    assert sample_transaction.amount == 100

def test_valid_transaction(sample_transaction):
    assert sample_transaction.validate()

def test_tampered_transaction(sample_transaction):
    sample_transaction.amount = 200
    assert not sample_transaction.validate()

def test_transaction_hashing_uniqueness():
    sender = BlockchainAccount()
    receiver = BlockchainAccount()
    tx1 = Transaction.create_transaction(sender, receiver.address, 100)
    tx2 = Transaction.create_transaction(sender, receiver.address, 200)
    assert tx1.txid != tx2.txid

@pytest.mark.parametrize("amount", [0, 1, 1000000, 999999])
def test_various_amounts(amount):
    sender = BlockchainAccount()
    receiver = BlockchainAccount()
    tx = Transaction.create_transaction(sender, receiver.address, amount)
    assert tx.validate()
    assert tx.amount == amount