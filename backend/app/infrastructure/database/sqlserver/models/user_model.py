from sqlalchemy import Column, DateTime, Enum, String, Boolean
from datetime import datetime

from app.infrastructure.database.sqlserver.models import Base
from app.domain.enums.role import RoleName


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleName), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
