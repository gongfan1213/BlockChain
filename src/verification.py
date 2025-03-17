from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from .merkle_tree import MerkleTree

class BlockchainVerifier:
    @staticmethod
    def verify_transaction(transaction, public_key):
        """验证交易签名"""
        try:
            transaction_hash = transaction.calculate_hash().encode()
            public_key.verify(
                transaction.signature,
                transaction_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
            
    @staticmethod
    def verify_chain(blockchain):
        """验证整个区块链"""
        for i in range(1, len(blockchain.chain)):
            current = blockchain.chain[i]
            previous = blockchain.chain[i-1]
            
            # 验证当前哈希
            if current.hash != current.calculate_hash():
                return False
                
            # 验证前一个哈希的链接
            if current.previous_hash != previous.hash:
                return False
                
            # 验证默克尔根
            merkle_tree = MerkleTree(current.transactions)
            if current.merkle_root != merkle_tree.build_tree():
                return False
                
        return True

    @staticmethod
    def verify_transactions_batch(transactions, public_keys):
        """批量验证交易"""
        if len(transactions) != len(public_keys):
            return False
        
        for tx, pk in zip(transactions, public_keys):
            if not BlockchainVerifier.verify_transaction(tx, pk):
                return False
        return True

    @staticmethod
    def verify_block_integrity(block):
        """验证单个区块的完整性"""
        # 验证区块哈希
        if block.hash != block.calculate_hash():
            return False
            
        # 验证所有交易
        merkle_tree = MerkleTree(block.transactions)
        if block.merkle_root != merkle_tree.build_tree():
            return False
            
        return True

    @staticmethod
    def detect_tampering(original_block, current_block):
        """检测区块是否被篡改"""
        tampering_info = {
            'is_tampered': False,
            'tampered_fields': []
        }
        
        # 检查区块哈希
        if original_block.hash != current_block.hash:
            tampering_info['is_tampered'] = True
            tampering_info['tampered_fields'].append('block_hash')
            
        # 检查交易列表
        if len(original_block.transactions) != len(current_block.transactions):
            tampering_info['is_tampered'] = True
            tampering_info['tampered_fields'].append('transactions_length')
        else:
            for i, (orig_tx, curr_tx) in enumerate(zip(original_block.transactions, current_block.transactions)):
                if orig_tx.transaction_id != curr_tx.transaction_id:
                    tampering_info['is_tampered'] = True
                    tampering_info['tampered_fields'].append(f'transaction_{i}')
                    
        # 检查时间戳
        if original_block.timestamp != current_block.timestamp:
            tampering_info['is_tampered'] = True
            tampering_info['tampered_fields'].append('timestamp')
            
        return tampering_info