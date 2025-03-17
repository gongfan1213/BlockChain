import pytest
from src.account import Account

def test_account_creation():
    account = Account()
    assert account.private_key is not None
    assert account.public_key is not None
    assert account.get_address() is not None

def test_account_signing():
    account = Account()
    message = "Test message"
    signature = account.sign(message)
    assert signature is not None

def test_different_accounts():
    account1 = Account()
    account2 = Account()
    assert account1.get_address() != account2.get_address()

def test_address_format():
    account = Account()
    address = account.get_address()
    assert isinstance(address, str)
    assert len(address) == 64  # SHA256 produces 32 bytes = 64 hex chars