from app.domain.interfaces.services.blockchain_client import BlockchainClient


class BlockchainService:

    def __init__(self, blockchain_client: BlockchainClient):
        self.blockchain_client = blockchain_client

    async def write_hash(self, batch_id: str, data_hash: str):
        return await self.blockchain_client.write_hash(batch_id, data_hash)

    async def get_hash(self, batch_id: str):
        return await self.blockchain_client.get_hash(batch_id)

    async def verify(self, batch_id: str, current_hash: str):
        blockchain_hash = await self.get_hash(batch_id)
        return {
            "batch_id": batch_id,
            "current_hash": current_hash,
            "blockchain_hash": blockchain_hash,
            "is_valid": current_hash == blockchain_hash,
        }
