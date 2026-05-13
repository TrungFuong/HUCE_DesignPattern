from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=1000)
    return _client


def get_mongo_database():
    return get_mongo_client()["ocop_traceability"]
