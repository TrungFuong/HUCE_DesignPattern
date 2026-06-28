from fastapi import APIRouter, Depends

from app.application.dto.farm_dto import CreateFarmRequest, UpdateFarmRequest
from app.application.services.farm_service import FarmService
from app.core.dependencies import get_current_user
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("/")
async def create_farm(
    request: CreateFarmRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
        return await farm_service.create_farm(request)


@router.get("/")
async def list_farms(
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
        return await farm_service.list_farms()


@router.get("/{farm_id}")
async def get_farm(
    farm_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
        return await farm_service.get_by_id(farm_id)


@router.put("/{farm_id}")
async def update_farm(
    farm_id: str,
    request: UpdateFarmRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
        return await farm_service.update_farm(farm_id, request)


@router.delete("/{farm_id}")
async def delete_farm(
    farm_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
        return await farm_service.delete_farm(farm_id)
