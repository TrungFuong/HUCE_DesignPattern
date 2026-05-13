from abc import ABC, abstractmethod


class MqttClient(ABC):

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback) -> None:
        pass
