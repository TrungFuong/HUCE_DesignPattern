from abc import ABC, abstractmethod

from app.domain.entities.farm import Farm


class FarmRepository(ABC):

    @abstractmethod
    async def find_by_id(self, farm_id: str) -> Farm | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Farm]:
        pass

    @abstractmethod
    async def find_by_owner_id(self, owner_id: str) -> list[Farm]:
        pass

    @abstractmethod
    async def save(self, farm: Farm) -> Farm:
        pass

    @abstractmethod
    async def update(self, farm: Farm) -> Farm:
        pass

    @abstractmethod
    async def delete(self, farm_id: str) -> None:
        pass
