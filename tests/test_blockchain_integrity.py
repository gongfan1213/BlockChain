"""Test cases for blockchain integrity verification"""
import pytest
from src.blockchain import Blockchain
from src.transaction import Transaction
from src.accounts import BlockchainAccount

@pytest.fixture
def blockchain():
    """Create a test blockchain instance"""
    return Blockchain(difficulty=2)

@pytest.fixture
def accounts():
    """Create test accounts"""
    return [BlockchainAccount() for _ in range(3)]

@pytest.fixture
def valid_transactions(accounts):
    """Create valid test transactions"""
    transactions = []
    for i in range(2):
        tx = Transaction.create_transaction(
            sender=accounts[i],
            receiver_address=accounts[i+1].address,
            amount=10
        )
        transactions.append(tx)
    return transactions

def test_transaction_integrity(blockchain, accounts, valid_transactions):
    """Test detection of transaction tampering"""
    # Add a block with valid transactions
    assert blockchain.add_block(valid_transactions)
    
    # Attempt to modify a transaction after block creation
    tampered_tx = valid_transactions[0]
    tampered_tx.amount = 100  # Modify amount
    
    # Verify chain integrity is broken
    assert not blockchain.is_chain_valid()

def test_block_integrity(blockchain, accounts, valid_transactions):
    """Test detection of block tampering"""
    # Add two blocks
    assert blockchain.add_block(valid_transactions)
    assert blockchain.add_block(valid_transactions)
    
    # Tamper with the first block's timestamp
    blockchain.chain[1].timestamp += 1000
    
    # Verify chain integrity is broken
    assert not blockchain.is_chain_valid()

def test_merkle_root_integrity(blockchain, accounts, valid_transactions):
    """Test detection of Merkle root tampering"""
    # Add a block
    assert blockchain.add_block(valid_transactions)
    
    # Tamper with the Merkle root
    original_merkle_root = blockchain.chain[1].merkle_root
    blockchain.chain[1].merkle_root = '0' * 64
    
    # Verify chain integrity is broken
    assert not blockchain.is_chain_valid()
    
    # Restore original Merkle root
    blockchain.chain[1].merkle_root = original_merkle_root
    
    # Verify chain integrity is restored
    assert blockchain.is_chain_valid()

def test_block_hash_chain_integrity(blockchain, accounts, valid_transactions):
    """Test detection of block hash chain tampering"""
    # Add three blocks
    for _ in range(3):
        assert blockchain.add_block(valid_transactions)
    
    # Tamper with middle block's previous_hash
    blockchain.chain[2].previous_hash = '0' * 64
    
    # Verify chain integrity is broken
    assert not blockchain.is_chain_valid()