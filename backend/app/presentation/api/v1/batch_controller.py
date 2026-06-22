from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.application.dto.batch_dto import CreateBatchRequest, UpdateBatchRequest
from app.application.services.batch_service import BatchService
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.qr.qr_code_service import QrCodeService
from app.core.dependencies import require_roles
from app.domain.entities.user import User
from app.domain.enums.role import RoleName

router = APIRouter(prefix="/batches", tags=["Batches"])


async def ensure_farmer_owns_farm(session, current_user: User, farm_id: str) -> None:
    if current_user.role != RoleName.FARMER:
        return
    farm = await SqlFarmRepository(session).find_by_id(farm_id)
    if farm is None or farm.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only use your own farms")


async def ensure_farmer_owns_batch(session, current_user: User, batch_id: str):
    batch = await SqlBatchRepository(session).find_by_id(batch_id)
    if batch is None:
        raise ValueError("Batch not found")
    await ensure_farmer_owns_farm(session, current_user, batch.farm_id)
    return batch


@router.post("/")
async def create_batch(
    request: CreateBatchRequest,
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        await ensure_farmer_owns_farm(session, current_user, request.farm_id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.create_batch(request)


@router.get("/")
async def list_batches(
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER, RoleName.TRADER)),
):
    async with get_async_session() as session:
        if current_user.role == RoleName.FARMER:
            return await SqlBatchRepository(session).find_by_owner_id(current_user.id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.list_batches()


@router.get("/{batch_id}")
async def get_batch(
    batch_id: str,
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER, RoleName.TRADER)),
):
    async with get_async_session() as session:
        await ensure_farmer_owns_batch(session, current_user, batch_id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.get_by_id(batch_id)


@router.put("/{batch_id}")
async def update_batch(
    batch_id: str,
    request: UpdateBatchRequest,
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        await ensure_farmer_owns_batch(session, current_user, batch_id)
        await ensure_farmer_owns_farm(session, current_user, request.farm_id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.update_batch(batch_id, request)


@router.delete("/{batch_id}")
async def delete_batch(
    batch_id: str,
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        await ensure_farmer_owns_batch(session, current_user, batch_id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.delete_batch(batch_id)


@router.post("/{batch_id}/qr")
async def regenerate_batch_qr(
    batch_id: str,
    current_user: User = Depends(require_roles(RoleName.ADMIN, RoleName.FARMER)),
):
    async with get_async_session() as session:
        await ensure_farmer_owns_batch(session, current_user, batch_id)
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        return await batch_service.regenerate_qr_code(batch_id)


@router.get("/{batch_id}/qr-image")
async def get_batch_qr_image(batch_id: str):
    async with get_async_session() as session:
        batch_service = BatchService(
            SqlBatchRepository(session),
            QrCodeService(),
            SqlFarmRepository(session),
            SqlCropTypeRepository(session),
            SqlShipmentRepository(session),
        )
        batch = await batch_service.regenerate_qr_code(batch_id)
        return FileResponse(batch.qr_code_url, media_type="image/png")
