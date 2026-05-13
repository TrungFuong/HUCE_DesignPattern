from sqlalchemy import Column, DateTime, Enum, String
from datetime import datetime

from app.infrastructure.database.sqlserver.models import Base
from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel


class BatchModel(Base):
    __tablename__ = "batches"

    id = Column(String(36), primary_key=True, index=True)
    farm_id = Column(String(36), nullable=False)
    product_name = Column(String(255), nullable=False)
    harvest_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(BatchStatus), nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    qr_code_url = Column(String(500), nullable=True)
