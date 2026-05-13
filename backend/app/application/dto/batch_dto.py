from datetime import datetime
from pydantic import BaseModel


class CreateBatchRequest(BaseModel):
    id: str | None = None
    farm_id: str
    product_name: str
    harvest_date: datetime


class BatchResponse(BaseModel):
    id: str
    farm_id: str
    product_name: str
    harvest_date: datetime
    status: str
    risk_level: str
    qr_code_url: str | None
