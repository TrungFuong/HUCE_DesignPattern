from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String, UniqueConstraint
from app.infrastructure.database.sqlserver.models import Base


class RiskRuleModel(Base):
    __tablename__ = "risk_rules"
    __table_args__ = (
        CheckConstraint("min_temperature <= max_temperature", name="ck_risk_rules_temperature_range"),
        CheckConstraint("min_humidity <= max_humidity", name="ck_risk_rules_humidity_range"),
        CheckConstraint(
            "min_soil_moisture IS NULL OR max_soil_moisture IS NULL OR min_soil_moisture <= max_soil_moisture",
            name="ck_risk_rules_soil_moisture_range",
        ),
        CheckConstraint("duration_minutes > 0", name="ck_risk_rules_duration_positive"),
        UniqueConstraint("crop_type_id", name="uq_risk_rules_crop_type_id"),
    )

    id = Column(String(36), primary_key=True, index=True)
    crop_type_id = Column(String(36), ForeignKey("crop_types.id"), nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)
    min_soil_moisture = Column(Float, nullable=True)
    max_soil_moisture = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
