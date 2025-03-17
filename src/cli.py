import click
import json
import os
from .blockchain import Blockchain
from .account import Account
from .transaction import Transaction
from .verification import BlockchainVerifier

@click.group()
def cli():
    """迷你区块链系统命令行工具"""
    pass

@cli.command()
@click.option('--difficulty', default=4, help='挖矿难度')
def init(difficulty):
    """初始化区块链"""
    blockchain = Blockchain(difficulty=difficulty)
    save_blockchain(blockchain)
    click.echo(f"区块链已初始化，难度设置为: {difficulty}")

@cli.command()
def create_account():
    """创建新账户"""
    account = Account()
    address = account.get_address()
    save_account(account, address)
    click.echo(f"账户已创建，地址: {address}")

@cli.command()
@click.argument('sender_address')
@click.argument('receiver_address')
@click.argument('amount', type=float)
def create_transaction(sender_address, receiver_address, amount):
    """创建新交易"""
    blockchain = load_blockchain()
    sender = load_account(sender_address)
    
    tx = Transaction(sender_address, receiver_address, amount)
    tx.sign_transaction(sender)
    blockchain.add_transaction(tx)
    save_blockchain(blockchain)
    
    click.echo(f"交易已创建: {tx.transaction_id}")

@cli.command()
@click.argument('miner_address')
def mine(miner_address):
    """挖掘新区块"""
    blockchain = load_blockchain()
    block = blockchain.mine_pending_transactions(miner_address)
    save_blockchain(blockchain)
    
    click.echo(f"新区块已挖出: {block.hash}")
    click.echo(f"包含 {len(block.transactions)} 笔交易")

@cli.command()
def verify():
    """验证区块链完整性"""
    blockchain = load_blockchain()
    verifier = BlockchainVerifier()
    
    if verifier.verify_chain(blockchain):
        click.echo("区块链验证通过")
    else:
        click.echo("区块链验证失败")

def save_blockchain(blockchain):
    """保存区块链状态"""
    data_dir = "d:\\code\\BlockChain\\data"
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "blockchain.json"), "w") as f:
        json.dump(blockchain.to_dict(), f)

def load_blockchain():
    """加载区块链状态"""
    data_dir = "d:\\code\\BlockChain\\data"
    blockchain_path = os.path.join(data_dir, "blockchain.json")
    if not os.path.exists(blockchain_path):
        return Blockchain()
    
    with open(blockchain_path, "r") as f:
        data = json.load(f)
        return Blockchain.from_dict(data)

def save_account(account, address):
    """保存账户信息"""
    accounts_dir = "d:\\code\\BlockChain\\data\\accounts"
    os.makedirs(accounts_dir, exist_ok=True)
    with open(os.path.join(accounts_dir, f"{address}.json"), "w") as f:
        json.dump({
            'address': address,
            'private_key': account.private_key.private_bytes(),
            'public_key': account.public_key.public_bytes()
        }, f)

def load_account(address):
    """加载账户信息"""
    accounts_dir = "d:\\code\\BlockChain\\data\\accounts"
    account_path = os.path.join(accounts_dir, f"{address}.json")
    if not os.path.exists(account_path):
        raise click.ClickException(f"账户不存在: {address}")
    
    with open(account_path, "r") as f:
        data = json.load(f)
        return Account.from_json(data)