from abc import ABC, abstractmethod


class QueueClient(ABC):

    @abstractmethod
    async def push(self, queue_name: str, data: dict) -> None:
        pass

    @abstractmethod
    async def pop(self, queue_name: str) -> dict | None:
        pass
