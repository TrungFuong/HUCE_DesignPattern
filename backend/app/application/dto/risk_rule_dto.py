from pydantic import BaseModel


class RiskRuleRequest(BaseModel):
    id: str | None = None
    crop_type_id: str
    min_temperature: float
    max_temperature: float
    min_humidity: float
    max_humidity: float
    min_soil_moisture: float | None = None
    max_soil_moisture: float | None = None
    duration_minutes: int


class RiskRuleResponse(BaseModel):
    id: str
    crop_type_id: str
    min_temperature: float
    max_temperature: float
    min_humidity: float
    max_humidity: float
    min_soil_moisture: float | None = None
    max_soil_moisture: float | None = None
    duration_minutes: int

    class Config:
        from_attributes = True

