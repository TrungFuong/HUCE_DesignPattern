from dataclasses import dataclass
from datetime import datetime


@dataclass
class Farm:
    id: str
    owner_id: str
    name: str
    address: str
    crop_type: str
    planting_date: datetime | None
    harvest_date: datetime | None
