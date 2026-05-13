from app.domain.entities.sensor_log import SensorLog
from app.domain.interfaces.repositories.sensor_log_repository import SensorLogRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError


class MongoSensorLogRepository(SensorLogRepository):

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.collection = mongo_db["sensor_logs"]

    async def save(self, sensor_log: SensorLog) -> SensorLog:
        document = sensor_log.__dict__.copy()
        await self.collection.insert_one(document)
        return sensor_log

    async def find_by_batch_id(self, batch_id: str) -> list[SensorLog]:
        try:
            cursor = self.collection.find({"batch_id": batch_id}).sort("recorded_at", 1)
            docs = await cursor.to_list(length=None)
        except PyMongoError:
            return []
        return [self._to_entity(doc) for doc in docs]

    async def find_recent_by_batch_id(self, batch_id: str, limit: int = 100) -> list[SensorLog]:
        try:
            cursor = self.collection.find({"batch_id": batch_id}).sort("recorded_at", -1).limit(limit)
            docs = await cursor.to_list(length=limit)
        except PyMongoError:
            return []
        return [self._to_entity(doc) for doc in docs]

    @staticmethod
    def _to_entity(document: dict) -> SensorLog:
        data = document.copy()
        data.pop("_id", None)
        return SensorLog(**data)
