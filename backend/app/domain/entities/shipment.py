from dataclasses import dataclass
from datetime import datetime


@dataclass
class Shipment:
    id: str
    batch_id: str
    distributor_id: str
    container_id: str
    origin: str
    destination: str
    start_time: datetime
    end_time: datetime | None
