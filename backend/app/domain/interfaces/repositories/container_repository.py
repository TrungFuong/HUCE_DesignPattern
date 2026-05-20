from abc import ABC, abstractmethod

from app.domain.entities.container import Container


class ContainerRepository(ABC):

    @abstractmethod
    async def find_by_id(self, container_id: str) -> Container | None:
        pass

    @abstractmethod
    async def find_by_code(self, code: str) -> Container | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Container]:
        pass

    @abstractmethod
    async def save(self, container: Container) -> Container:
        pass

    @abstractmethod
    async def update(self, container: Container) -> Container:
        pass

    @abstractmethod
    async def delete(self, container_id: str) -> bool:
        pass
