from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorLog:
    id: str
    batch_id: str
    temperature: float
    humidity: float
    soil_moisture: float | None
    recorded_at: datetime
