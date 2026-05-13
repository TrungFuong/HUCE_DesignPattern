from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.infrastructure.database.sqlserver.models import Base

# Import model modules so SQLAlchemy registers every table in Base.metadata.
from app.infrastructure.database.sqlserver.models import batch_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import container_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import farm_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import risk_rule_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import shipment_model  # noqa: F401
from app.infrastructure.database.sqlserver.models import user_model  # noqa: F401


engine = create_async_engine(settings.sqlserver_url, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_async_session() -> AsyncSession:
    return async_session()


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
