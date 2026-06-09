from sqlalchemy import Boolean, CheckConstraint, Column, Float, Integer, String, Unicode
from app.infrastructure.database.sqlserver.models import Base


class ContainerModel(Base):
    __tablename__ = "containers"
    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_containers_capacity_positive"),
        CheckConstraint(
            "min_temperature IS NULL OR max_temperature IS NULL OR min_temperature <= max_temperature",
            name="ck_containers_temperature_range",
        ),
    )

    id = Column(String(36), primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)
    type = Column(Unicode(100), nullable=False)
    capacity = Column(Float, nullable=False)
    capacity_unit = Column(Unicode(20), nullable=False, default="kg")
    material = Column(Unicode(100), nullable=True)
    is_temperature_controlled = Column(Boolean, nullable=False, default=False)
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    status = Column(Integer, nullable=False, default=0)
    description = Column(Unicode(500), nullable=True)
