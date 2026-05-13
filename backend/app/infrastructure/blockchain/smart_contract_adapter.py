from app.domain.interfaces.services.blockchain_client import BlockchainClient
from app.infrastructure.blockchain.web3_client import Web3Client
from web3.contract import Contract


class SmartContractAdapter(BlockchainClient):

    def __init__(self, web3: Web3Client, contract: Contract | None):
        self.web3 = web3
        self.contract = contract

    async def write_hash(self, batch_id: str, data_hash: str) -> str:
        if self.contract is None:
            return ""
        transaction = self.contract.functions.storeHash(batch_id, data_hash).build_transaction({
            "from": self.web3.web3.eth.default_account,
        })
        tx_hash = self.web3.web3.eth.send_transaction(transaction)
        return tx_hash.hex()

    async def get_hash(self, batch_id: str) -> str | None:
        if self.contract is None:
            return None
        return self.contract.functions.getHash(batch_id).call()
