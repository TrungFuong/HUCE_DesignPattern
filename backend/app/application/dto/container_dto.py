from pydantic import BaseModel


class CreateContainerRequest(BaseModel):
    id: str | None = None
    code: str
    type: str
    capacity: float
    capacity_unit: str = "kg"
    material: str | None = None
    is_temperature_controlled: bool = False
    min_temperature: float | None = None
    max_temperature: float | None = None
    status: int | str = 0
    description: str | None = None


class UpdateContainerRequest(BaseModel):
    code: str | None = None
    type: str | None = None
    capacity: float | None = None
    capacity_unit: str | None = None
    material: str | None = None
    is_temperature_controlled: bool | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    status: int | str | None = None
    description: str | None = None


class ContainerResponse(BaseModel):
    id: str
    code: str
    type: str
    capacity: float
    capacity_unit: str
    material: str | None = None
    is_temperature_controlled: bool
    min_temperature: float | None = None
    max_temperature: float | None = None
    status: int
    description: str | None = None
