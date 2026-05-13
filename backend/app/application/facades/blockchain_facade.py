class BlockchainFacade:

    def __init__(self, blockchain_service):
        self.blockchain_service = blockchain_service

    async def write_hash(self, batch_id: str, data_hash: str) -> str:
        return await self.blockchain_service.write_hash(batch_id, data_hash)

    async def get_hash(self, batch_id: str) -> str | None:
        return await self.blockchain_service.get_hash(batch_id)
