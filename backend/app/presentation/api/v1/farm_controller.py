from fastapi import APIRouter
from app.application.dto.farm_dto import CreateFarmRequest
from app.application.services.farm_service import FarmService
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("/")
async def create_farm(request: CreateFarmRequest):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session))
        return await farm_service.create_farm(request)
