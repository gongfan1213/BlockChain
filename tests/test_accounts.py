"""
Account Module Tests
Verifies ECC key generation and transaction signing/verification
"""
import pytest
from src.accounts import BlockchainAccount

def test_account_creation():
    account = BlockchainAccount()
    assert len(account.private_key.to_string()) == 32
    assert len(account.address) == 128

def test_signature_verification():
    sender = BlockchainAccount()
    receiver = BlockchainAccount()
    test_data = b"test_message"
    
    signature = sender.sign_transaction(test_data)
    assert BlockchainAccount.verify_signature(
        sender.address,
        signature,
        test_data
    )
    
    assert not BlockchainAccount.verify_signature(
        receiver.address,
        signature,
        test_data
    )

@pytest.mark.parametrize("data", [b"", b"123", b"large_data"*100])
def test_various_data_signing(data):
    account = BlockchainAccount()
    sig = account.sign_transaction(data)
    assert BlockchainAccount.verify_signature(account.address, sig, data)