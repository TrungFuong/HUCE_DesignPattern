from sqlalchemy import select

from app.domain.entities.shipment import Shipment
from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository
from app.infrastructure.database.sqlserver.models.shipment_model import ShipmentModel


class SqlShipmentRepository(ShipmentRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_by_id(self, shipment_id: str) -> Shipment | None:
        model = await self.db_session.get(ShipmentModel, shipment_id)
        if model is None:
            return None
        return Shipment(
            id=model.id,
            batch_id=model.batch_id,
            distributor_id=model.distributor_id,
            container_id=model.container_id,
            origin=model.origin,
            destination=model.destination,
            start_time=model.start_time,
            end_time=model.end_time,
        )

    async def save(self, shipment: Shipment) -> Shipment:
        model = ShipmentModel(
            id=shipment.id,
            batch_id=shipment.batch_id,
            distributor_id=shipment.distributor_id,
            container_id=shipment.container_id,
            origin=shipment.origin,
            destination=shipment.destination,
            start_time=shipment.start_time,
            end_time=shipment.end_time,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return shipment

    async def find_by_batch_id(self, batch_id: str) -> Shipment | None:
        result = await self.db_session.execute(select(ShipmentModel).where(ShipmentModel.batch_id == batch_id))
        model = result.scalars().first()
        if model is None:
            return None
        return Shipment(
            id=model.id,
            batch_id=model.batch_id,
            distributor_id=model.distributor_id,
            container_id=model.container_id,
            origin=model.origin,
            destination=model.destination,
            start_time=model.start_time,
            end_time=model.end_time,
        )
