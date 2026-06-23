from app.domain.interfaces.services.blockchain_client import BlockchainClient
from app.infrastructure.queue.redis_client import get_redis_client
from redis.exceptions import RedisError


class BlockchainProxy(BlockchainClient):

    def __init__(self, blockchain_client: BlockchainClient, cache_client=None):
        self.blockchain_client = blockchain_client
        self.cache_client = cache_client or get_redis_client()

    async def get_hash(self, batch_id: str) -> str | None:
        cache_key = f"blockchain_hash:{batch_id}"
        try:
            cached_hash = await self.cache_client.get(cache_key)
            if cached_hash:
                # decode_responses=True → Redis always returns str, not bytes
                return cached_hash
        except RedisError:
            cached_hash = None
        blockchain_hash = await self.blockchain_client.get_hash(batch_id)
        if blockchain_hash and cached_hash is None:
            try:
                await self.cache_client.set(cache_key, blockchain_hash, ex=300)
            except RedisError:
                pass
        elif blockchain_hash:
            await self.cache_client.set(cache_key, blockchain_hash, ex=300)
        return blockchain_hash

    async def write_hash(self, batch_id: str, data_hash: str) -> str:
        tx_hash = await self.blockchain_client.write_hash(batch_id, data_hash)
        try:
            await self.cache_client.delete(f"blockchain_hash:{batch_id}")
        except RedisError:
            pass
        return tx_hash
