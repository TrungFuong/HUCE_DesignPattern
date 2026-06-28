from abc import ABC, abstractmethod

from app.domain.entities.batch_chemical import BatchChemical


class BatchChemicalRepository(ABC):

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[BatchChemical]:
        pass

    @abstractmethod
    async def save_all(self, items: list[BatchChemical]) -> list[BatchChemical]:
        pass

    @abstractmethod
    async def delete_by_batch_id(self, batch_id: str) -> None:
        pass
