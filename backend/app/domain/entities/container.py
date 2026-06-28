from dataclasses import dataclass

from app.domain.enums.container_status import ContainerStatus


@dataclass
class Container:
    id: str
    code: str
    type: str
    capacity: float
    capacity_unit: str
    material: str | None = None
    is_temperature_controlled: bool = False
    min_temperature: float | None = None
    max_temperature: float | None = None
    status: ContainerStatus = ContainerStatus.ACTIVE
    description: str | None = None
