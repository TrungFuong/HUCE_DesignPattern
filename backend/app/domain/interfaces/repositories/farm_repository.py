from abc import ABC, abstractmethod

from app.domain.entities.farm import Farm


class FarmRepository(ABC):

    @abstractmethod
    async def find_by_id(self, farm_id: str) -> Farm | None:
        pass

    @abstractmethod
    async def save(self, farm: Farm) -> Farm:
        pass
