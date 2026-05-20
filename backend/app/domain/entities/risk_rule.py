from dataclasses import dataclass


@dataclass
class RiskRule:
    id: str
    crop_type_id: str
    min_temperature: float
    max_temperature: float
    min_humidity: float
    max_humidity: float
    min_soil_moisture: float | None
    max_soil_moisture: float | None
    duration_minutes: int
