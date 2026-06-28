from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.application.dto.batch_dto import CreateBatchRequest, UpdateBatchRequest
from app.application.services.batch_service import BatchService
from app.core.dependencies import get_batch_service, get_current_user
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.qr.qr_code_service import QrCodeService

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("/")
async def create_batch(
    request: CreateBatchRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.create_batch(request)


@router.get("/")
async def list_batches(
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.list_batches()


@router.get("/{batch_id}")
async def get_batch(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.get_by_id(batch_id)


@router.put("/{batch_id}")
async def update_batch(
    batch_id: str,
    request: UpdateBatchRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.update_batch(batch_id, request)


@router.delete("/{batch_id}")
async def delete_batch(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.delete_batch(batch_id)


@router.post("/{batch_id}/qr")
async def regenerate_batch_qr(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        return await batch_service.regenerate_qr_code(batch_id)


@router.get("/{batch_id}/qr-image")
async def get_batch_qr_image(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
        )
        batch = await batch_service.regenerate_qr_code(batch_id)
        return FileResponse(batch.qr_code_url, media_type="image/png")
