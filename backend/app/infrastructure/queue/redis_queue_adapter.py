import json

from app.domain.interfaces.services.queue_client import QueueClient
from app.infrastructure.queue.redis_client import get_redis_client


class RedisQueueAdapter(QueueClient):

    def __init__(self, client=None):
        self.client = client or get_redis_client()

    async def push(self, queue_name: str, data: dict) -> None:
        await self.client.rpush(queue_name, json.dumps(data))

    async def pop(self, queue_name: str) -> dict | None:
        raw = await self.client.lpop(queue_name)
        if raw is None:
            return None
        return json.loads(raw)
