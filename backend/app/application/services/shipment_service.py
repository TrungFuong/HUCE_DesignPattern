import uuid

from app.application.utils.enum_parser import format_enum_options, parse_enum
from app.domain.entities.shipment import Shipment, ShipmentItem
from app.domain.enums.shipment_status import ShipmentStatus
from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.domain.interfaces.repositories.container_repository import ContainerRepository
from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository
from app.domain.interfaces.repositories.user_repository import UserRepository


class ShipmentService:

    def __init__(
        self,
        shipment_repository: ShipmentRepository,
        batch_repository: BatchRepository | None = None,
        user_repository: UserRepository | None = None,
        container_repository: ContainerRepository | None = None,
    ):
        self.shipment_repository = shipment_repository
        self.batch_repository = batch_repository
        self.user_repository = user_repository
        self.container_repository = container_repository

    def _parse_status(self, status: int | str | None) -> ShipmentStatus:
        if status is None or status == "":
            return ShipmentStatus.CREATED
        try:
            return parse_enum(ShipmentStatus, status)
        except (KeyError, ValueError) as error:
            valid_statuses = format_enum_options(ShipmentStatus)
            raise ValueError(f"Invalid shipment status. Use one of: {valid_statuses}") from error

    async def create_shipment(self, data):
        await self._validate_foreign_keys(data)
        await self._validate_items(data.items, data.id)
        self._validate_required_text(data.origin, "Shipment origin")
        self._validate_required_text(data.destination, "Shipment destination")
        if data.end_time and data.end_time < data.start_time:
            raise ValueError("Shipment end_time must be after start_time")

        shipment_id = data.id or str(uuid.uuid4())
        shipment = Shipment(
            id=shipment_id,
            from_actor_id=data.from_actor_id,
            to_actor_id=data.to_actor_id,
            carrier_id=data.carrier_id,
            origin=data.origin,
            destination=data.destination,
            status=self._parse_status(data.status),
            start_time=data.start_time,
            end_time=data.end_time,
            notes=data.notes,
        )
        saved = await self.shipment_repository.save(shipment)
        for item_data in data.items:
            item = ShipmentItem(
                id=item_data.id or str(uuid.uuid4()),
                shipment_id=shipment_id,
                batch_id=item_data.batch_id,
                container_id=item_data.container_id,
                quantity=item_data.quantity,
                quantity_unit=item_data.quantity_unit,
            )
            await self.shipment_repository.save_item(item)
        return await self.get_with_items(saved.id)

    async def get_by_batch_id(self, batch_id: str):
        shipments = await self.shipment_repository.find_by_batch_id(batch_id)
        return [await self._shipment_with_items(shipment) for shipment in shipments]

    async def get_by_id(self, shipment_id: str):
        shipment = await self.shipment_repository.find_by_id(shipment_id)
        if shipment is None:
            raise ValueError("Shipment not found")
        return shipment

    async def get_with_items(self, shipment_id: str):
        shipment = await self.get_by_id(shipment_id)
        return await self._shipment_with_items(shipment)

    async def _shipment_with_items(self, shipment: Shipment) -> dict:
        result = shipment.__dict__.copy()
        result["items"] = [
            item.__dict__
            for item in await self.shipment_repository.find_items_by_shipment_id(shipment.id)
        ]
        return result

    async def _validate_foreign_keys(self, data) -> None:
        if self.user_repository:
            for field_name in ["from_actor_id", "to_actor_id", "carrier_id"]:
                user_id = getattr(data, field_name)
                user = await self.user_repository.find_by_id(user_id)
                if user is None:
                    raise ValueError(f"Shipment {field_name} does not exist")
        if data.from_actor_id == data.to_actor_id:
            raise ValueError("Shipment from_actor_id and to_actor_id must be different")

    async def _validate_items(self, items, shipment_id: str | None) -> None:
        if not items:
            raise ValueError("Shipment must have at least one item")

        container_totals: dict[str, float] = {}
        seen_lines: set[tuple[str, str]] = set()
        for item in items:
            self._validate_positive_quantity(item.quantity, "Shipment item quantity")
            self._validate_required_text(item.quantity_unit, "Shipment item quantity unit")
            line_key = (item.batch_id, item.container_id)
            if line_key in seen_lines:
                raise ValueError("Duplicate shipment item for the same batch and container")
            seen_lines.add(line_key)

            batch = await self._get_batch(item.batch_id)
            container = await self._get_container(item.container_id)
            if batch.quantity_unit != item.quantity_unit:
                raise ValueError("Shipment item quantity_unit must match batch quantity_unit")
            if container.capacity_unit != item.quantity_unit:
                raise ValueError("Shipment item quantity_unit must match container capacity_unit")

            already_shipped = await self.shipment_repository.sum_quantity_by_batch_id(item.batch_id, shipment_id)
            same_request_quantity = sum(
                other.quantity for other in items if other.batch_id == item.batch_id
            )
            if already_shipped + same_request_quantity > batch.quantity:
                raise ValueError("Shipment item quantity exceeds remaining batch quantity")

            container_totals[item.container_id] = container_totals.get(item.container_id, 0) + item.quantity
            if container_totals[item.container_id] > container.capacity:
                raise ValueError("Shipment item quantity exceeds container capacity")

    async def _get_batch(self, batch_id: str):
        if self.batch_repository is None:
            raise ValueError("Batch repository is required for shipment validation")
        batch = await self.batch_repository.find_by_id(batch_id)
        if batch is None:
            raise ValueError("Shipment item batch_id does not exist")
        return batch

    async def _get_container(self, container_id: str):
        if self.container_repository is None:
            raise ValueError("Container repository is required for shipment validation")
        container = await self.container_repository.find_by_id(container_id)
        if container is None:
            raise ValueError("Shipment item container_id does not exist")
        return container

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")

    def _validate_positive_quantity(self, value: float, field_name: str) -> None:
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
