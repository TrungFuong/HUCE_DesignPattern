from app.domain.entities.blockchain_record import BlockchainRecord
from app.domain.interfaces.repositories.blockchain_repository import BlockchainRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class MongoBlockchainRecordRepository(BlockchainRepository):

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.collection = mongo_db["blockchain_records"]

    async def save(self, record: BlockchainRecord) -> BlockchainRecord:
        await self.collection.insert_one(record.__dict__.copy())
        return record

    async def find_by_batch_id(self, batch_id: str) -> list[BlockchainRecord]:
        docs = await self.collection.find({"batch_id": batch_id}).to_list(length=None)
        return [self._to_entity(doc) for doc in docs]

    @staticmethod
    def _to_entity(document: dict) -> BlockchainRecord:
        data = document.copy()
        data.pop("_id", None)
        return BlockchainRecord(**data)
