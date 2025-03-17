from click.testing import CliRunner
from src.cli import cli
import os
import pytest

@pytest.fixture
def runner():
    return CliRunner()

def test_init_blockchain(runner):
    result = runner.invoke(cli, ['init', '--difficulty', '4'])
    assert result.exit_code == 0
    assert "区块链已初始化" in result.output

def test_create_account(runner):
    result = runner.invoke(cli, ['create-account'])
    assert result.exit_code == 0
    assert "账户已创建" in result.output
    assert "地址:" in result.output

def test_create_transaction(runner):
    # 创建测试账户
    result = runner.invoke(cli, ['create-account'])
    sender_address = result.output.split(': ')[1].strip()
    result = runner.invoke(cli, ['create-account'])
    receiver_address = result.output.split(': ')[1].strip()
    
    # 创建交易
    result = runner.invoke(cli, [
        'create-transaction',
        sender_address,
        receiver_address,
        '100'
    ])
    assert result.exit_code == 0
    assert "交易已创建" in result.output

def test_mine_block(runner):
    # 创建账户和交易
    result = runner.invoke(cli, ['create-account'])
    miner_address = result.output.split(': ')[1].strip()
    
    result = runner.invoke(cli, ['mine', miner_address])
    assert result.exit_code == 0
    assert "新区块已挖出" in result.output

def test_verify_chain(runner):
    result = runner.invoke(cli, ['verify'])
    assert result.exit_code == 0
    assert "区块链验证" in result.output