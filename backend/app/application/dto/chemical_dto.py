from datetime import datetime

from pydantic import BaseModel


class ChemicalRequest(BaseModel):
    crop_type_id: str
    name: str
    unit: str
    description: str | None = None


class ChemicalResponse(BaseModel):
    id: str
    crop_type_id: str
    name: str
    unit: str
    description: str | None = None


class BatchChemicalItem(BaseModel):
    chemical_id: str
    applied_at: datetime | None = None


class BatchChemicalResponse(BaseModel):
    chemical_id: str
    applied_at: datetime | None = None
