from web3 import Web3
from web3.contract import Contract


TRACEABILITY_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "dataHash", "type": "string"},
        ],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "batchId", "type": "string"}],
        "name": "getHash",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]


class Web3Client:

    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

    def get_contract(self, contract_address: str) -> Contract | None:
        if not contract_address:
            return None
        return self.web3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=TRACEABILITY_CONTRACT_ABI,
        )
