from sqlalchemy import Column, DateTime, String
from app.infrastructure.database.sqlserver.models import Base


class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(String(36), primary_key=True, index=True)
    batch_id = Column(String(36), nullable=False)
    distributor_id = Column(String(36), nullable=False)
    container_id = Column(String(36), nullable=False)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
