from sqlalchemy import Boolean, Column, ForeignKey, String, Unicode

from app.infrastructure.database.sqlserver.models import Base


class ChemicalModel(Base):
    __tablename__ = "chemicals"

    id = Column(String(36), primary_key=True, index=True)
    crop_type_id = Column(String(36), ForeignKey("crop_types.id"), nullable=False, index=True)
    name = Column(Unicode(255), nullable=False)
    unit = Column(Unicode(50), nullable=False)
    description = Column(Unicode(500), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
