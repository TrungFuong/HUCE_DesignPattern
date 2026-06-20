from sqlalchemy import delete, func, select

from app.application.utils.enum_parser import parse_enum
from app.domain.entities.shipment import Shipment, ShipmentItem
from app.domain.enums.shipment_status import ShipmentStatus
from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository
from app.infrastructure.database.sqlserver.models.shipment_model import ShipmentItemModel, ShipmentModel


class SqlShipmentRepository(ShipmentRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def _to_shipment(self, model: ShipmentModel) -> Shipment:
        return Shipment(
            id=model.id,
            from_actor_id=model.from_actor_id,
            to_actor_id=model.to_actor_id,
            carrier_id=model.carrier_id,
            origin=model.origin,
            destination=model.destination,
            status=parse_enum(ShipmentStatus, model.status),
            start_time=model.start_time,
            end_time=model.end_time,
            notes=model.notes,
        )

    def _to_item(self, model: ShipmentItemModel) -> ShipmentItem:
        return ShipmentItem(
            id=model.id,
            shipment_id=model.shipment_id,
            batch_id=model.batch_id,
            container_id=model.container_id,
            quantity=model.quantity,
            quantity_unit=model.quantity_unit,
        )

    async def find_by_id(self, shipment_id: str) -> Shipment | None:
        model = await self.db_session.get(ShipmentModel, shipment_id)
        if model is None:
            return None
        return self._to_shipment(model)

    async def find_all(self) -> list[Shipment]:
        result = await self.db_session.execute(select(ShipmentModel).order_by(ShipmentModel.start_time.desc()))
        return [self._to_shipment(model) for model in result.scalars().all()]

    async def save(self, shipment: Shipment) -> Shipment:
        model = ShipmentModel(
            id=shipment.id,
            from_actor_id=shipment.from_actor_id,
            to_actor_id=shipment.to_actor_id,
            carrier_id=shipment.carrier_id,
            origin=shipment.origin,
            destination=shipment.destination,
            status=int(shipment.status),
            start_time=shipment.start_time,
            end_time=shipment.end_time,
            notes=shipment.notes,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return shipment

    async def update(self, shipment: Shipment) -> Shipment:
        model = await self.db_session.get(ShipmentModel, shipment.id)
        if model is None:
            return await self.save(shipment)
        model.from_actor_id = shipment.from_actor_id
        model.to_actor_id = shipment.to_actor_id
        model.carrier_id = shipment.carrier_id
        model.origin = shipment.origin
        model.destination = shipment.destination
        model.status = int(shipment.status)
        model.start_time = shipment.start_time
        model.end_time = shipment.end_time
        model.notes = shipment.notes
        await self.db_session.commit()
        return shipment

    async def delete(self, shipment_id: str) -> None:
        model = await self.db_session.get(ShipmentModel, shipment_id)
        if model is None:
            raise ValueError("Shipment not found")
        await self.db_session.execute(delete(ShipmentItemModel).where(ShipmentItemModel.shipment_id == shipment_id))
        await self.db_session.delete(model)
        await self.db_session.commit()

    async def save_item(self, item: ShipmentItem) -> ShipmentItem:
        model = ShipmentItemModel(
            id=item.id,
            shipment_id=item.shipment_id,
            batch_id=item.batch_id,
            container_id=item.container_id,
            quantity=item.quantity,
            quantity_unit=item.quantity_unit,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return item

    async def replace_items(self, shipment_id: str, items: list[ShipmentItem]) -> None:
        await self.db_session.execute(delete(ShipmentItemModel).where(ShipmentItemModel.shipment_id == shipment_id))
        for item in items:
            self.db_session.add(
                ShipmentItemModel(
                    id=item.id,
                    shipment_id=item.shipment_id,
                    batch_id=item.batch_id,
                    container_id=item.container_id,
                    quantity=item.quantity,
                    quantity_unit=item.quantity_unit,
                )
            )
        await self.db_session.commit()

    async def find_by_batch_id(self, batch_id: str) -> list[Shipment]:
        result = await self.db_session.execute(
            select(ShipmentModel)
            .join(ShipmentItemModel, ShipmentItemModel.shipment_id == ShipmentModel.id)
            .where(ShipmentItemModel.batch_id == batch_id)
            .order_by(ShipmentModel.start_time.asc())
            .distinct()
        )
        return [self._to_shipment(model) for model in result.scalars().all()]

    async def find_items_by_shipment_id(self, shipment_id: str) -> list[ShipmentItem]:
        result = await self.db_session.execute(
            select(ShipmentItemModel).where(ShipmentItemModel.shipment_id == shipment_id)
        )
        return [self._to_item(model) for model in result.scalars().all()]

    async def find_items_by_batch_id(self, batch_id: str) -> list[ShipmentItem]:
        result = await self.db_session.execute(
            select(ShipmentItemModel).where(ShipmentItemModel.batch_id == batch_id)
        )
        return [self._to_item(model) for model in result.scalars().all()]

    async def sum_quantity_by_batch_id(self, batch_id: str, exclude_shipment_id: str | None = None) -> float:
        query = select(func.coalesce(func.sum(ShipmentItemModel.quantity), 0.0)).where(
            ShipmentItemModel.batch_id == batch_id
        )
        if exclude_shipment_id:
            query = query.where(ShipmentItemModel.shipment_id != exclude_shipment_id)
        result = await self.db_session.execute(query)
        return float(result.scalar_one() or 0)

    async def sum_quantity_by_shipment_and_container_id(self, shipment_id: str, container_id: str) -> float:
        result = await self.db_session.execute(
            select(func.coalesce(func.sum(ShipmentItemModel.quantity), 0.0))
            .where(ShipmentItemModel.shipment_id == shipment_id)
            .where(ShipmentItemModel.container_id == container_id)
        )
        return float(result.scalar_one() or 0)

    async def exists_by_container_id(self, container_id: str) -> bool:
        result = await self.db_session.execute(
            select(ShipmentItemModel.id)
            .where(ShipmentItemModel.container_id == container_id)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
