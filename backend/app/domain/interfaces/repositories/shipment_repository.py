from abc import ABC, abstractmethod

from app.domain.entities.shipment import Shipment


class ShipmentRepository(ABC):

    @abstractmethod
    async def find_by_id(self, shipment_id: str) -> Shipment | None:
        pass

    @abstractmethod
    async def save(self, shipment: Shipment) -> Shipment:
        pass

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> Shipment | None:
        pass
