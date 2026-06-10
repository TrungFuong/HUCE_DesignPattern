from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, String, Unicode
from datetime import datetime

from app.infrastructure.database.sqlserver.models import Base


class FarmModel(Base):
    __tablename__ = "farms"
    __table_args__ = (
        CheckConstraint(
            "planting_date IS NULL OR harvest_date IS NULL OR harvest_date >= planting_date",
            name="ck_farms_harvest_after_planting",
        ),
        Index("ix_farms_owner_id", "owner_id"),
    )

    id = Column(String(36), primary_key=True, index=True)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(Unicode(255), nullable=False)
    address = Column(Unicode(500), nullable=False)
    planting_date = Column(DateTime, nullable=True)
    harvest_date = Column(DateTime, nullable=True)
