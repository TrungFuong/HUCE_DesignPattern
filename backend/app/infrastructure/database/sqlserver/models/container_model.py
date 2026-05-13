from sqlalchemy import Column, String
from app.infrastructure.database.sqlserver.models import Base


class ContainerModel(Base):
    __tablename__ = "containers"

    id = Column(String(36), primary_key=True, index=True)
    code = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
