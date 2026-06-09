from abc import ABC, abstractmethod

from app.domain.entities.batch import Batch


class BatchRepository(ABC):

    @abstractmethod
    async def find_by_id(self, batch_id: str) -> Batch | None:
        pass

    @abstractmethod
    async def save(self, batch: Batch) -> Batch:
        pass

    @abstractmethod
    async def find_all(self) -> list[Batch]:
        pass

    @abstractmethod
    async def update(self, batch: Batch) -> Batch:
        pass

    @abstractmethod
    async def delete(self, batch_id: str) -> None:
        pass

    @abstractmethod
    async def find_by_farm_id(self, farm_id: str) -> list[Batch]:
        pass
