# Mini Blockchain Implementation

## 1. Introduction
This project implements a mini blockchain system in Python. It includes core components such as account management, transaction processing, and Merkle tree construction.

## 2. Implemented Features
### 2.1 Account Management
- ECC key generation
- Transaction signing and verification

### 2.2 Transaction Processing
- Transaction creation
- Signature verification

### 2.3 Testing
- Unit tests for account management
- Unit tests for transaction processing

## 3. Code Structure
```
src/
  accounts.py        # Account management
  transaction.py     # Transaction processing
  merkle_tree.py      # Merkle tree implementation
tests/
  test_accounts.py    # Unit tests for accounts
  test_transaction.py # Unit tests for transactions
```

## 4. Running the Code
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run tests:
```
pytest tests/
pip install ecdsa
python -m pytest
```

