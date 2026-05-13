from abc import ABC, abstractmethod


class BlockchainClient(ABC):

    @abstractmethod
    async def write_hash(self, batch_id: str, data_hash: str) -> str:
        pass

    @abstractmethod
    async def get_hash(self, batch_id: str) -> str | None:
        pass
