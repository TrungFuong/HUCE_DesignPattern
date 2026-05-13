from sqlalchemy import Column, DateTime, String
from datetime import datetime

from app.infrastructure.database.sqlserver.models import Base


class FarmModel(Base):
    __tablename__ = "farms"

    id = Column(String(36), primary_key=True, index=True)
    owner_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    crop_type = Column(String(100), nullable=False)
    planting_date = Column(DateTime, nullable=True)
    harvest_date = Column(DateTime, nullable=True)
