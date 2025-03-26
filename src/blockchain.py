"""
blockchain.py

Blockchain Construction Module

Implements blockchain structure with proof-of-work mining and Merkle tree integration.
"""
import time
from hashlib import sha256
from typing import List
from .merkle_tree import MerkleTree
from .transaction import Transaction

class Block:
    """Represents a block in the blockchain containing multiple transactions."""
    
    def __init__(self, index: int, previous_hash: str, transactions: List[Transaction], difficulty: int):
        """
        Initialize a new block.

        Args:
            index (int): Block index (height)
            previous_hash (str): Hash of the previous block
            transactions (List[Transaction]): List of transactions in the block
            difficulty (int): Proof-of-work difficulty target (leading zeros)
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = 0
        self.merkle_root = self._calculate_merkle_root()
        self.hash = self.calculate_hash()

    def _calculate_merkle_root(self) -> str:
        """Calculate Merkle root hash from transaction IDs."""
        if not self.transactions:
            return sha256(b'').hexdigest()
        tx_ids = [tx.txid for tx in self.transactions]
        return MerkleTree(tx_ids).root_hash

    def calculate_hash(self) -> str:
        """Calculate the block's cryptographic hash using header data."""
        header_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}{self.difficulty}"
        return sha256(header_data.encode()).hexdigest()

    def mine(self) -> None:
        """Perform proof-of-work mining to find a valid hash."""
        while not self.is_valid_hash():
            self.nonce += 1
            self.hash = self.calculate_hash()

    def is_valid_hash(self) -> bool:
        """Check if the block's hash meets the difficulty target."""
        return self.hash.startswith('0' * self.difficulty)

class Blockchain:
    """Manages the blockchain containing a sequence of validated blocks."""
    
    def __init__(self, difficulty: int = 2):
        """Initialize blockchain with genesis block."""
        self.difficulty = difficulty
        self.chain = [self._create_genesis_block()]

    def _create_genesis_block(self) -> Block:
        """Generate the genesis block (first block in the chain)."""
        return Block(
            index=0,
            previous_hash="0",
            transactions=[],
            difficulty=self.difficulty
        )

    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]

    def add_block(self, transactions: List[Transaction]) -> bool:
        """
        Mine and add a new block to the chain after validating:
        - Valid transactions
        - Correct Merkle root
        - Valid proof-of-work
        - Proper chain linkage
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            transactions=transactions,
            difficulty=self.difficulty
        )
        new_block.mine()

        # Validate transactions
        for tx in transactions:
            if not tx.validate():
                print("Invalid transaction signature")
                return False

        # Validate Merkle root
        tx_ids = [tx.txid for tx in transactions]
        expected_merkle_root = MerkleTree(tx_ids).root_hash
        if new_block.merkle_root != expected_merkle_root:
            print("Merkle root mismatch")
            return False

        # Validate block integrity
        if not self._is_block_valid(new_block, latest_block):
            print("Block validation failed")
            return False

        self.chain.append(new_block)
        return True

    def _is_block_valid(self, new_block: Block, previous_block: Block) -> bool:
        """Validate block structure and proof-of-work."""
        if new_block.index != previous_block.index + 1:
            return False
        if new_block.previous_hash != previous_block.hash:
            return False
        if not new_block.is_valid_hash():
            return False
        return True

    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if not self._is_block_valid(current_block, previous_block):
                return False

            # Re-validate all transactions
            for tx in current_block.transactions:
                if not tx.validate():
                    return False

            # Re-calculate Merkle root
            tx_ids = [tx.txid for tx in current_block.transactions]
            if MerkleTree(tx_ids).root_hash != current_block.merkle_root:
                return False

        return True