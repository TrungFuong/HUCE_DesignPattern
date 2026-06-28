from fastapi import APIRouter, Depends

from app.application.dto.crop_type_dto import CropTypeRequest
from app.application.services.crop_type_service import CropTypeService
from app.core.dependencies import get_current_user
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/crop-types", tags=["Crop Types"])


@router.post("/")
async def create_crop_type(
    request: CropTypeRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        crop_type_service = CropTypeService(SqlCropTypeRepository(session))
        return await crop_type_service.create_crop_type(request)


@router.get("/")
async def list_crop_types(
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        crop_type_service = CropTypeService(SqlCropTypeRepository(session))
        return await crop_type_service.list_crop_types()


@router.get("/{code}")
async def get_crop_type(
    code: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        crop_type_service = CropTypeService(SqlCropTypeRepository(session))
        return await crop_type_service.get_by_code(code)


@router.put("/{crop_type_id}")
async def update_crop_type(
    crop_type_id: str,
    request: CropTypeRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        crop_type_service = CropTypeService(SqlCropTypeRepository(session))
        return await crop_type_service.update_crop_type(crop_type_id, request)


@router.delete("/{crop_type_id}")
async def delete_crop_type(
    crop_type_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        crop_type_service = CropTypeService(SqlCropTypeRepository(session))
        return await crop_type_service.delete_crop_type(crop_type_id)
