from datetime import datetime
from pydantic import BaseModel


class CreateBatchRequest(BaseModel):
    id: str | None = None
    farm_id: str
    crop_type_id: str
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str = "kg"
    grade: str | None = None


class BatchResponse(BaseModel):
    id: str
    farm_id: str
    crop_type_id: str
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str
    grade: str | None
    status: int
    risk_level: int
    qr_code_url: str | None
