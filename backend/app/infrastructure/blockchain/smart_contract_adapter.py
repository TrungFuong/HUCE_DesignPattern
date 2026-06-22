import asyncio

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
        return await asyncio.to_thread(self._write_hash_sync, batch_id, data_hash)

    def _write_hash_sync(self, batch_id: str, data_hash: str) -> str:
        w3 = self.web3.web3
        from_account = w3.eth.accounts[0] if w3.eth.accounts else w3.eth.default_account
        transaction = self.contract.functions.storeHash(batch_id, data_hash).build_transaction({
            "from": from_account,
            "nonce": w3.eth.get_transaction_count(from_account),
            "gas": 200000,
        })
        tx_hash = w3.eth.send_transaction(transaction)
        return tx_hash.hex()

    async def get_hash(self, batch_id: str) -> str | None:
        if self.contract is None:
            return None
        return await asyncio.to_thread(self._get_hash_sync, batch_id)

    def _get_hash_sync(self, batch_id: str) -> str | None:
        result = self.contract.functions.getHash(batch_id).call()
        return result if result else None
