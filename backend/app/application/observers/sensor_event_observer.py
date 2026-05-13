from abc import ABC, abstractmethod


class SensorEventObserver(ABC):

    @abstractmethod
    async def update(self, sensor_log):
        pass
