from abc import ABC, abstractmethod


class QrService(ABC):

    @abstractmethod
    async def generate_for_batch(self, batch_id: str) -> str:
        pass
