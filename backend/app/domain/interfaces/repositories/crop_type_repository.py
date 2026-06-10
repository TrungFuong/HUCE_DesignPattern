from abc import ABC, abstractmethod

from app.domain.entities.crop_type import CropType


class CropTypeRepository(ABC):

    @abstractmethod
    async def find_by_id(self, crop_type_id: str) -> CropType | None:
        pass

    @abstractmethod
    async def find_by_code(self, code: str) -> CropType | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[CropType]:
        pass

    @abstractmethod
    async def save(self, crop_type: CropType) -> CropType:
        pass

    @abstractmethod
    async def update(self, crop_type: CropType) -> CropType:
        pass

    @abstractmethod
    async def delete(self, crop_type_id: str) -> None:
        pass
