from fastapi import APIRouter, Depends

from app.application.dto.crop_type_dto import CropTypeRequest
from app.application.services.crop_type_service import CropTypeService
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName

router = APIRouter(prefix="/crop-types", tags=["Crop Types"])


def create_crop_type_service(session) -> CropTypeService:
    return CropTypeService(
        SqlCropTypeRepository(session),
        SqlBatchRepository(session),
        SqlRiskRuleRepository(session),
    )


@router.post("/", dependencies=[Depends(require_roles(RoleName.ADMIN))])
async def create_crop_type(request: CropTypeRequest):
    async with get_async_session() as session:
        crop_type_service = create_crop_type_service(session)
        return await crop_type_service.create_crop_type(request)


@router.get("/", dependencies=[Depends(require_roles(RoleName.ADMIN, RoleName.FARMER, RoleName.TRADER))])
async def list_crop_types():
    async with get_async_session() as session:
        crop_type_service = create_crop_type_service(session)
        return await crop_type_service.list_crop_types()


@router.get("/{code}", dependencies=[Depends(require_roles(RoleName.ADMIN, RoleName.FARMER, RoleName.TRADER))])
async def get_crop_type(code: str):
    async with get_async_session() as session:
        crop_type_service = create_crop_type_service(session)
        return await crop_type_service.get_by_code(code)


@router.put("/{crop_type_id}", dependencies=[Depends(require_roles(RoleName.ADMIN))])
async def update_crop_type(crop_type_id: str, request: CropTypeRequest):
    async with get_async_session() as session:
        crop_type_service = create_crop_type_service(session)
        return await crop_type_service.update_crop_type(crop_type_id, request)


@router.delete("/{crop_type_id}", dependencies=[Depends(require_roles(RoleName.ADMIN))])
async def delete_crop_type(crop_type_id: str):
    async with get_async_session() as session:
        crop_type_service = create_crop_type_service(session)
        return await crop_type_service.delete_crop_type(crop_type_id)
