from fastapi import APIRouter, Depends

from app.application.dto.crop_type_dto import CropTypeRequest
from app.application.services.crop_type_service import CropTypeService
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/crop-types", tags=["Crop Types"])


def create_crop_type_service(session) -> CropTypeService:
    return CropTypeService(
        SqlCropTypeRepository(session),
        SqlBatchRepository(session),
        SqlRiskRuleRepository(session),
    )


@router.post("/")
async def create_crop_type(
    request: CropTypeRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        return await create_crop_type_service(session).create_crop_type(request)


@router.get("/")
async def list_crop_types(
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        return await create_crop_type_service(session).list_crop_types()


@router.get("/{code}")
async def get_crop_type(
    code: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        return await create_crop_type_service(session).get_by_code(code)


@router.put("/{crop_type_id}")
async def update_crop_type(
    crop_type_id: str,
    request: CropTypeRequest,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        return await create_crop_type_service(session).update_crop_type(crop_type_id, request)


@router.delete("/{crop_type_id}")
async def delete_crop_type(
    crop_type_id: str,
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    async with get_async_session() as session:
        return await create_crop_type_service(session).delete_crop_type(crop_type_id)
