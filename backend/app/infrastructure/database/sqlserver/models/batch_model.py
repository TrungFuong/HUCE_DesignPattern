from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Index, Integer, String
from datetime import datetime

from app.infrastructure.database.sqlserver.models import Base


class BatchModel(Base):
    __tablename__ = "batches"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_batches_quantity_positive"),
        Index("ix_batches_farm_id", "farm_id"),
    )

    id = Column(String(36), primary_key=True, index=True)
    farm_id = Column(String(36), ForeignKey("farms.id"), nullable=False)
    crop_type_id = Column(String(36), ForeignKey("crop_types.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    harvest_date = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Float, nullable=False)
    quantity_unit = Column(String(20), nullable=False, default="kg")
    grade = Column(String(50), nullable=True)
    status = Column(Integer, nullable=False)
    risk_level = Column(Integer, nullable=False)
    qr_code_url = Column(String(500), nullable=True)
