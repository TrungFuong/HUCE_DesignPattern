from abc import ABC, abstractmethod

from app.domain.entities.blockchain_record import BlockchainRecord


class BlockchainRepository(ABC):

    @abstractmethod
    async def save(self, record: BlockchainRecord) -> BlockchainRecord:
        pass

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[BlockchainRecord]:
        pass
