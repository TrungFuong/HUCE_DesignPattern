from abc import ABC, abstractmethod

from app.domain.entities.sensor_log import SensorLog


class SensorLogRepository(ABC):

    @abstractmethod
    async def save(self, sensor_log: SensorLog) -> SensorLog:
        pass

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[SensorLog]:
        pass

    @abstractmethod
    async def find_recent_by_batch_id(self, batch_id: str, limit: int = 100) -> list[SensorLog]:
        pass
