from datetime import datetime
from pydantic import BaseModel


class CreateShipmentRequest(BaseModel):
    id: str | None = None
    batch_id: str
    distributor_id: str
    container_id: str
    origin: str
    destination: str
    start_time: datetime
    end_time: datetime | None = None
