import uuid

from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository
from app.domain.entities.shipment import Shipment


class ShipmentService:

    def __init__(self, shipment_repository: ShipmentRepository):
        self.shipment_repository = shipment_repository

    async def create_shipment(self, data):
        shipment = Shipment(
            id=data.id or str(uuid.uuid4()),
            batch_id=data.batch_id,
            distributor_id=data.distributor_id,
            container_id=data.container_id,
            origin=data.origin,
            destination=data.destination,
            start_time=data.start_time,
            end_time=data.end_time,
        )
        return await self.shipment_repository.save(shipment)

    async def get_by_batch_id(self, batch_id: str):
        return await self.shipment_repository.find_by_batch_id(batch_id)
