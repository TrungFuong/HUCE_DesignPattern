from datetime import datetime
from pydantic import BaseModel


class ShipmentItemRequest(BaseModel):
    id: str | None = None
    batch_id: str
    container_id: str
    quantity: float
    quantity_unit: str = "kg"


class CreateShipmentRequest(BaseModel):
    id: str | None = None
    from_actor_id: str
    to_actor_id: str
    carrier_id: str
    origin: str
    destination: str
    status: int | str = 0
    start_time: datetime
    end_time: datetime | None = None
    notes: str | None = None
    items: list[ShipmentItemRequest]
