from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.shipment_status import ShipmentStatus


@dataclass
class Shipment:
    id: str
    from_actor_id: str
    to_actor_id: str
    carrier_id: str
    origin: str
    destination: str
    status: ShipmentStatus
    start_time: datetime
    end_time: datetime | None
    notes: str | None = None


@dataclass
class ShipmentItem:
    id: str
    shipment_id: str
    batch_id: str
    container_id: str
    quantity: float
    quantity_unit: str
