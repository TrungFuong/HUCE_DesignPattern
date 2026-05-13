from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.database.sqlserver.models import Base


class RiskRuleModel(Base):
    __tablename__ = "risk_rules"

    id = Column(String(36), primary_key=True, index=True)
    crop_type = Column(String(100), nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)
    min_soil_moisture = Column(Float, nullable=True)
    max_soil_moisture = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
