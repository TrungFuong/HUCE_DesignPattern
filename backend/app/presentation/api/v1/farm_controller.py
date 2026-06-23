from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.farm_dto import CreateFarmRequest, UpdateFarmRequest
from app.application.services.farm_service import FarmService
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/farms", tags=["Farms"])


def create_farm_service(session) -> FarmService:
    return FarmService(
        SqlFarmRepository(session),
        SqlUserRepository(session),
        SqlBatchRepository(session),
    )


@router.post("/")
async def create_farm(
    request: CreateFarmRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        if current_user["role"] == int(RoleName.FARMER):
            request = request.model_copy(update={"owner_id": current_user["id"]})
        return await create_farm_service(session).create_farm(request)


@router.get("/")
async def list_farms(
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        if current_user["role"] == int(RoleName.FARMER):
            return await SqlFarmRepository(session).find_by_owner_id(current_user["id"])
        return await create_farm_service(session).list_farms()


@router.get("/{farm_id}")
async def get_farm(
    farm_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        farm = await create_farm_service(session).get_by_id(farm_id)
        if current_user["role"] == int(RoleName.FARMER) and farm.owner_id != current_user["id"]:
            raise HTTPException(status_code=403, detail="You can only access your own farms")
        return farm


@router.put("/{farm_id}")
async def update_farm(
    farm_id: str,
    request: UpdateFarmRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        farm_service = create_farm_service(session)
        existing = await farm_service.get_by_id(farm_id)
        if current_user["role"] == int(RoleName.FARMER):
            if existing.owner_id != current_user["id"]:
                raise HTTPException(status_code=403, detail="You can only update your own farms")
            request = request.model_copy(update={"owner_id": current_user["id"]})
        return await farm_service.update_farm(farm_id, request)


@router.delete("/{farm_id}")
async def delete_farm(
    farm_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        farm_service = create_farm_service(session)
        existing = await farm_service.get_by_id(farm_id)
        if current_user["role"] == int(RoleName.FARMER) and existing.owner_id != current_user["id"]:
            raise HTTPException(status_code=403, detail="You can only delete your own farms")
        return await farm_service.delete_farm(farm_id)
