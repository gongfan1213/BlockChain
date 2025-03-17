import hashlib
# 默克尔树实现模块
class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = []
        
    def build_tree(self):
        """构建默克尔树"""
        # 获取交易哈希列表
        transaction_hashes = [tx.transaction_id for tx in self.transactions]
        
        # 确保交易数量是2的幂
        while len(transaction_hashes) > 1:
            temp_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                if i + 1 < len(transaction_hashes):
                    combined = transaction_hashes[i] + transaction_hashes[i+1]
                    new_hash = hashlib.sha256(combined.encode()).hexdigest()
                    temp_hashes.append(new_hash)
                else:
                    temp_hashes.append(transaction_hashes[i])
            transaction_hashes = temp_hashes
            self.tree.append(transaction_hashes)
            
        return transaction_hashes[0]  # 返回根哈希