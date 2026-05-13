from datetime import datetime
from pydantic import BaseModel


class SensorLogRequest(BaseModel):
    id: str
    batch_id: str
    temperature: float
    humidity: float
    soil_moisture: float | None = None
    recorded_at: datetime
