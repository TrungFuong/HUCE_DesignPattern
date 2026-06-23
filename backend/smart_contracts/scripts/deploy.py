"""
Script deploy TraceabilityContract lên Ganache local.

Cach chay:
    cd backend
    python smart_contracts/scripts/deploy.py

Yeu cau:
    - Ganache dang chay tai http://127.0.0.1:7545
    - web3 da cai (co trong requirements.txt)
    - py-solc-x se tu dong download solc neu chua co

Sau khi chay xong:
    - Copy contract_address vao .env
    - Copy private_key tu Ganache vao .env
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOL_FILE = ROOT / "smart_contracts" / "TraceabilityContract.sol"

try:
    from web3 import Web3
    from solcx import compile_source, install_solc
except ImportError as e:
    print(f"Thieu thu vien: {e}")
    print("Chay: pip install py-solc-x web3")
    sys.exit(1)


RPC_URL = "http://127.0.0.1:7545"


def deploy():
    # 1. Ket noi Ganache
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print(f"[ERROR] Khong ket noi duoc voi Ganache tai {RPC_URL}")
        print("  -> Mo Ganache Desktop va click QUICKSTART truoc.")
        sys.exit(1)

    print(f"[OK] Ket noi Ganache: {RPC_URL}")
    accounts = w3.eth.accounts
    print(f"[OK] Tim thay {len(accounts)} accounts")
    deployer = accounts[0]
    print(f"[OK] Deploying tu account: {deployer}")

    # 2. Compile contract
    install_solc("0.8.0")
    source = SOL_FILE.read_text(encoding="utf-8")
    compiled = compile_source(source, output_values=["abi", "bin"], solc_version="0.8.0")
    contract_id = list(compiled.keys())[0]
    abi = compiled[contract_id]["abi"]
    bytecode = compiled[contract_id]["bin"]
    print(f"[OK] Compile contract thanh cong: {contract_id}")

    # 3. Deploy
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({"from": deployer})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    print(f"\n{'='*50}")
    print(f"[SUCCESS] Contract deployed!")
    print(f"  contract_address = {contract_address}")
    print(f"{'='*50}")
    print(f"\nCap nhat file .env:")
    print(f"  contract_address={contract_address}")
    print(f"\nPrivate key: Lay tu Ganache GUI (bam icon chiec khoa ben cai account dau tien)")
    print(f"  blockchain_rpc_url=http://127.0.0.1:7545")

    # 4. Luu ABI ra file de tham khao
    abi_path = ROOT / "smart_contracts" / "TraceabilityContract.abi.json"
    abi_path.write_text(json.dumps(abi, indent=2), encoding="utf-8")
    print(f"\nABI da luu tai: {abi_path}")

    return contract_address


if __name__ == "__main__":
    deploy()
