from fastapi import APIRouter
from app.application.dto.farm_dto import CreateFarmRequest
from app.application.services.farm_service import FarmService
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("/")
async def create_farm(request: CreateFarmRequest):
    async with get_async_session() as session:
        farm_service = FarmService(
            SqlFarmRepository(session),
            SqlUserRepository(session),
        )
        return await farm_service.create_farm(request)


@router.get("/{farm_id}")
async def get_farm(farm_id: str):
    async with get_async_session() as session:
        farm_service = FarmService(
            SqlFarmRepository(session),
            SqlUserRepository(session),
        )
        return await farm_service.get_by_id(farm_id)
