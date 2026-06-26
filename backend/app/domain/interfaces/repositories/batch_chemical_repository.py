from abc import ABC, abstractmethod

from app.domain.entities.batch_chemical import BatchChemical


class BatchChemicalRepository(ABC):

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[BatchChemical]:
        pass

    @abstractmethod
    async def save_all(self, items: list[BatchChemical]) -> list[BatchChemical]:
        """Lưu toàn bộ danh sách hóa chất cho một batch (replace)."""
        pass

    @abstractmethod
    async def delete_by_batch_id(self, batch_id: str) -> None:
        """Xóa mềm toàn bộ hóa chất của một batch (để chuẩn bị replace)."""
        pass
