from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.infrastructure.database.sqlserver.models import Base

# Import model modules so SQLAlchemy registers every table in Base.metadata.
from app.infrastructure.database.sqlserver.models import batch_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import container_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import crop_type_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import farm_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import risk_rule_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import shipment_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import user_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import chemical_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import batch_chemical_model  # noqa: F401


engine = create_async_engine(settings.sqlserver_url, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_async_session() -> AsyncSession:
    return async_session()


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(text("ALTER TABLE batches ALTER COLUMN crop_type_id VARCHAR(36) NULL"))
        unicode_columns = [
            ("users", "full_name", "NVARCHAR(255)", "NOT NULL"),
            ("farms", "name", "NVARCHAR(255)", "NOT NULL"),
            ("farms", "address", "NVARCHAR(500)", "NOT NULL"),
            ("batches", "product_name", "NVARCHAR(255)", "NOT NULL"),
            ("batches", "quantity_unit", "NVARCHAR(20)", "NOT NULL"),
            ("batches", "grade", "NVARCHAR(50)", "NULL"),
            ("crop_types", "name", "NVARCHAR(255)", "NOT NULL"),
            ("crop_types", "description", "NVARCHAR(500)", "NULL"),
            ("shipments", "origin", "NVARCHAR(255)", "NOT NULL"),
            ("shipments", "destination", "NVARCHAR(255)", "NOT NULL"),
            ("shipments", "notes", "NVARCHAR(500)", "NULL"),
            ("shipment_items", "quantity_unit", "NVARCHAR(20)", "NOT NULL"),
            ("containers", "type", "NVARCHAR(100)", "NOT NULL"),
            ("containers", "capacity_unit", "NVARCHAR(20)", "NOT NULL"),
            ("containers", "material", "NVARCHAR(100)", "NULL"),
            ("containers", "description", "NVARCHAR(500)", "NULL"),
        ]

        for table_name, column_name, column_type, nullability in unicode_columns:
            await connection.execute(
                text(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {column_type} {nullability}")
            )
