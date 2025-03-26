"""
Blockchain Test Module

Contains example usage and test cases for the blockchain system.
"""
import pytest
from src.accounts import BlockchainAccount
from src.transaction import Transaction
from src.blockchain import Blockchain


def test_blockchain_system():
    # Initialize test accounts
    alice = BlockchainAccount()
    bob = BlockchainAccount()

    print("=== Account Initialization ===")
    print(f"Alice's Address: {alice.address[:16]}...")
    print(f"Bob's Address:   {bob.address[:16]}...\n")

    # Create transactions
    print("=== Create Transactions ===")
    tx1 = Transaction.create_transaction(alice, bob.address, 50)
    tx2 = Transaction.create_transaction(bob, alice.address, 30)

    print(f"Transaction 1 ID: {tx1.txid[:16]}... Validation Result: {tx1.validate()}")
    print(f"Transaction 2 ID: {tx2.txid[:16]}... Validation Result: {tx2.validate()}\n")

    # Initialize the blockchain
    blockchain = Blockchain(difficulty=2)  # Set a lower mining difficulty for testing

    print("=== Create Genesis Block ===")
    print(f"Genesis Block Hash: {blockchain.chain[0].hash[:16]}...\n")

    # Add the first block
    print("=== Mining... Add the First Block ===")
    if blockchain.add_block([tx1, tx2]):
        latest = blockchain.get_latest_block()
        print(f"Block #{latest.index} Added Successfully!")
        print(f"Block Hash: {latest.hash[:16]}...")
        print(f"Nonce Value: {latest.nonce}")
        print(f"Number of Transactions: {len(latest.transactions)}\n")

    # Add the second empty block
    print("=== Mining... Add the Second Empty Block ===")
    if blockchain.add_block([]):  # Test an empty block
        latest = blockchain.get_latest_block()
        print(f"Block #{latest.index} Added Successfully!")
        print(f"Block Hash: {latest.hash[:16]}...\n")

    # Verify the integrity of the blockchain
    print("=== Blockchain Verification ===")
    print(f"Is the blockchain valid? {blockchain.is_chain_valid()}")
    print(f"Current chain length: {len(blockchain.chain)}")

    # Print the complete blockchain
    print("\n=== Complete Blockchain Structure ===")
    for block in blockchain.chain:
        print(f"Block #{block.index} [{block.hash[:16]}...]")
        print(f"Previous Hash: {block.previous_hash[:16]}...")
        print(f"Number of Transactions: {len(block.transactions)}")
        print(f"Merkle Root: {block.merkle_root[:16]}...")
        print("-----------------------")