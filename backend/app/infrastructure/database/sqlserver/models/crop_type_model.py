from sqlalchemy import Column, String, UniqueConstraint, Unicode

from app.infrastructure.database.sqlserver.models import Base


class CropTypeModel(Base):
    __tablename__ = "crop_types"
    __table_args__ = (
        UniqueConstraint("code", name="uq_crop_types_code"),
    )

    id = Column(String(36), primary_key=True, index=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(500), nullable=True)
