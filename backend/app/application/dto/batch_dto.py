from datetime import datetime
from typing import List
from pydantic import BaseModel


class CreateBatchRequest(BaseModel):
    id: str | None = None
    farm_id: str
    crop_type_id: str | None = None
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str = "kg"
    grade: str | None = None


class UpdateBatchRequest(BaseModel):
    farm_id: str
    crop_type_id: str | None = None
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str = "kg"
    grade: str | None = None


class BatchResponse(BaseModel):
    id: str
    farm_id: str
    crop_type_id: str | None
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str
    grade: str | None
    status: int
    risk_level: int
    qr_code_url: str | None


class BatchChemicalSummary(BaseModel):
    chemical_id: str
    applied_at: datetime | None = None


class BatchDetailResponse(BatchResponse):
    """Response đầy đủ của batch, bao gồm danh sách hóa chất đã sử dụng."""
    chemicals: List[BatchChemicalSummary] = []
