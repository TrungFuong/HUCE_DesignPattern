from datetime import datetime
from pydantic import BaseModel


class CreateFarmRequest(BaseModel):
    id: str | None = None
    owner_id: str
    name: str
    address: str
    planting_date: datetime | None = None
    harvest_date: datetime | None = None


class UpdateFarmRequest(BaseModel):
    owner_id: str
    name: str
    address: str
    planting_date: datetime | None = None
    harvest_date: datetime | None = None


class FarmResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    address: str
    planting_date: datetime | None
    harvest_date: datetime | None
