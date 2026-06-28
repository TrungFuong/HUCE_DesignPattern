from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, PrimaryKeyConstraint, String

from app.infrastructure.database.sqlserver.models import Base


class BatchChemicalModel(Base):
    __tablename__ = "batch_chemicals"
    __table_args__ = (
        PrimaryKeyConstraint("batch_id", "chemical_id", name="pk_batch_chemicals"),
    )

    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False, index=True)
    chemical_id = Column(String(36), ForeignKey("chemicals.id"), nullable=False, index=True)
    applied_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)
