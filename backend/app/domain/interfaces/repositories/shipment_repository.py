from abc import ABC, abstractmethod

from app.domain.entities.shipment import Shipment, ShipmentItem


class ShipmentRepository(ABC):

    @abstractmethod
    async def find_by_id(self, shipment_id: str) -> Shipment | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Shipment]:
        pass

    @abstractmethod
    async def find_by_to_actor_id(self, actor_id: str) -> list[Shipment]:
        pass

    @abstractmethod
    async def save(self, shipment: Shipment) -> Shipment:
        pass

    @abstractmethod
    async def update(self, shipment: Shipment) -> Shipment:
        pass

    @abstractmethod
    async def delete(self, shipment_id: str) -> None:
        pass

    @abstractmethod
    async def save_item(self, item: ShipmentItem) -> ShipmentItem:
        pass

    @abstractmethod
    async def replace_items(self, shipment_id: str, items: list[ShipmentItem]) -> None:
        pass

    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[Shipment]:
        pass

    @abstractmethod
    async def find_items_by_shipment_id(self, shipment_id: str) -> list[ShipmentItem]:
        pass

    @abstractmethod
    async def find_items_by_batch_id(self, batch_id: str) -> list[ShipmentItem]:
        pass

    @abstractmethod
    async def sum_quantity_by_batch_id(self, batch_id: str, exclude_shipment_id: str | None = None) -> float:
        pass

    @abstractmethod
    async def sum_quantity_by_shipment_and_container_id(self, shipment_id: str, container_id: str) -> float:
        pass

    @abstractmethod
    async def exists_by_container_id(self, container_id: str) -> bool:
        pass
