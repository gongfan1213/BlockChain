"""
Merkle Tree Module
Implements verifiable Merkle tree structure with SHA-256 hashing
"""
from hashlib import sha256
from typing import List

class MerkleTree:
    def __init__(self, transactions: List[str]):
        """Initialize Merkle tree with given transactions"""
        if not transactions:
            transactions = [""]  # Add an empty string as a leaf node to avoid empty list situations
        if len(transactions) % 2 != 0:
            transactions.append(transactions[-1])

        self.transactions = transactions
        self.tree = self.build_tree(transactions)

    @staticmethod
    def hash_pair(left: str, right: str) -> str:
        """Hash two nodes together using SHA-256"""
        combined = left + right
        return sha256(combined.encode()).hexdigest()

    def build_tree(self, nodes: List[str]) -> List[List[str]]:
        """Build the Merkle tree from leaf nodes"""
        tree = [nodes]
        while len(nodes) > 1:
            new_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i+1] if i+1 < len(nodes) else left
                new_level.append(self.hash_pair(left, right))
            tree.append(new_level)
            nodes = new_level
        return tree

    @property
    def root_hash(self) -> str:
        """Get the root hash of the Merkle tree"""
        if self.tree:  # Add a check to see if self.tree is empty
            return self.tree[-1][0]
        else:
            return ""  # If empty, return an empty string

    def get_proof(self, index: int) -> List[str]:
        """Get the Merkle proof for a transaction at given index"""
        proof = []
        current_level = 0
        current_index = index
        
        while current_level < len(self.tree)-1:
            sibling_index = current_index + 1 if current_index % 2 == 0 else current_index - 1
            if sibling_index < len(self.tree[current_level]):
                proof.append(self.tree[current_level][sibling_index])
            current_index = current_index // 2
            current_level += 1
        
        return proof

    def verify_proof(self, transaction_hash: str, proof: List[str]) -> bool:
        """Verify a transaction using its Merkle proof"""
        current_hash = transaction_hash
        for sibling_hash in proof:
            current_hash = sha256((current_hash + sibling_hash).encode()).hexdigest()
        return current_hash == self.root_hash