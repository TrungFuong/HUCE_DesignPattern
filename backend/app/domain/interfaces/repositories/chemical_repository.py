from abc import ABC, abstractmethod

from app.domain.entities.chemical import Chemical


class ChemicalRepository(ABC):

    @abstractmethod
    async def find_by_id(self, chemical_id: str) -> Chemical | None:
        pass

    @abstractmethod
    async def find_by_crop_type_id(self, crop_type_id: str) -> list[Chemical]:
        pass

    @abstractmethod
    async def find_all(self) -> list[Chemical]:
        pass

    @abstractmethod
    async def save(self, chemical: Chemical) -> Chemical:
        pass

    @abstractmethod
    async def update(self, chemical: Chemical) -> Chemical:
        pass

    @abstractmethod
    async def soft_delete(self, chemical_id: str) -> None:
        pass

    @abstractmethod
    async def is_used_by_batch(self, chemical_id: str) -> bool:
        """Trả về True nếu hóa chất đang được dùng bởi ít nhất 1 batch."""
        pass
