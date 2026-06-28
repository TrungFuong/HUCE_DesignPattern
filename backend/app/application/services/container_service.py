import uuid

from app.application.dto.container_dto import CreateContainerRequest, UpdateContainerRequest
from app.application.utils.enum_parser import format_enum_options, parse_enum
from app.domain.entities.container import Container
from app.domain.enums.container_status import ContainerStatus
from app.domain.interfaces.repositories.container_repository import ContainerRepository
from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository


class ContainerService:

    def __init__(
        self,
        container_repository: ContainerRepository,
        shipment_repository: ShipmentRepository | None = None,
    ):
        self.container_repository = container_repository
        self.shipment_repository = shipment_repository

    async def create_container(self, data: CreateContainerRequest) -> Container:
        self._validate_required_text(data.code, "Container code")
        self._validate_required_text(data.type, "Container type")
        self._validate_positive_quantity(data.capacity, "Container capacity")
        self._validate_required_text(data.capacity_unit, "Container capacity unit")
        self._validate_temperature_range(data.min_temperature, data.max_temperature)
        await self._validate_unique_code(data.code)
        container = Container(
            id=data.id or str(uuid.uuid4()),
            code=data.code,
            type=data.type,
            capacity=data.capacity,
            capacity_unit=data.capacity_unit,
            material=data.material,
            is_temperature_controlled=data.is_temperature_controlled,
            min_temperature=data.min_temperature,
            max_temperature=data.max_temperature,
            status=self._parse_status(data.status),
            description=data.description,
        )
        return await self.container_repository.save(container)

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")

    def _validate_positive_quantity(self, value: float, field_name: str) -> None:
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    def _validate_temperature_range(self, min_temperature: float | None, max_temperature: float | None) -> None:
        if min_temperature is not None and max_temperature is not None and min_temperature > max_temperature:
            raise ValueError("min_temperature must be less than or equal to max_temperature")

    def _parse_status(self, status: int | str | None) -> ContainerStatus:
        if status is None or status == "":
            return ContainerStatus.ACTIVE
        try:
            return parse_enum(ContainerStatus, status)
        except (KeyError, ValueError) as error:
            valid_statuses = format_enum_options(ContainerStatus)
            raise ValueError(f"Invalid container status. Use one of: {valid_statuses}") from error

    async def _validate_unique_code(self, code: str, current_container_id: str | None = None) -> None:
        existing = await self.container_repository.find_by_code(code)
        if existing and existing.id != current_container_id:
            raise ValueError("Container code already exists")

    async def get_by_id(self, container_id: str) -> Container:
        container = await self.container_repository.find_by_id(container_id)
        if container is None:
            raise ValueError("Container not found")
        return container

    async def list_containers(self) -> list[Container]:
        return await self.container_repository.find_all()

    async def update_container(self, container_id: str, data: UpdateContainerRequest) -> Container:
        container = await self.get_by_id(container_id)
        if data.code is not None:
            self._validate_required_text(data.code, "Container code")
            await self._validate_unique_code(data.code, container_id)
            container.code = data.code
        if data.type is not None:
            self._validate_required_text(data.type, "Container type")
            container.type = data.type
        if data.capacity is not None:
            self._validate_positive_quantity(data.capacity, "Container capacity")
            container.capacity = data.capacity
        if data.capacity_unit is not None:
            self._validate_required_text(data.capacity_unit, "Container capacity unit")
            container.capacity_unit = data.capacity_unit
        if data.material is not None:
            container.material = data.material
        if data.is_temperature_controlled is not None:
            container.is_temperature_controlled = data.is_temperature_controlled
        if data.min_temperature is not None:
            container.min_temperature = data.min_temperature
        if data.max_temperature is not None:
            container.max_temperature = data.max_temperature
        if data.status is not None:
            container.status = self._parse_status(data.status)
        self._validate_temperature_range(container.min_temperature, container.max_temperature)
        if data.description is not None:
            container.description = data.description
        return await self.container_repository.update(container)

    async def delete_container(self, container_id: str) -> dict[str, bool]:
        if self.shipment_repository and await self.shipment_repository.exists_by_container_id(container_id):
            raise ValueError("Container is being used by shipments")
        deleted = await self.container_repository.delete(container_id)
        if not deleted:
            raise ValueError("Container not found")
        return {"deleted": True}
