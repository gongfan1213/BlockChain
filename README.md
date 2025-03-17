# BlockChain Mini System

## 项目概述
这是一个基于Python实现的迷你区块链系统，实现了以下核心功能：
- 交易生成与验证
- 可验证的默克尔树
- 区块链构建
- 工作量证明挖矿
- 完整性验证

## 环境要求
- Python 3.8+
- cryptography
- pytest
- python-dateutil

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt

# 测试配置文件pytest.ini
# 初始化区块链
python main.py init --difficulty 4

# 创建账户
python main.py create-account

# 创建交易
python main.py create-transaction <sender_address> <receiver_address> 100

# 挖矿
python main.py mine <miner_address>

# 验证区块链
python main.py verify
