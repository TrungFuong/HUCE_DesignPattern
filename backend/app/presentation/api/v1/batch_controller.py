from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from typing import List

from app.application.dto.batch_dto import (
    CreateBatchRequest,
    UpdateBatchRequest,
    BatchDetailResponse,
    BatchChemicalSummary,
)
from app.application.dto.chemical_dto import BatchChemicalItem, BatchChemicalResponse
from app.application.services.batch_service import BatchService
from app.core.dependencies import get_current_user, require_roles
from app.domain.enums.role import RoleName
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_batch_chemical_repository import SqlBatchChemicalRepository
from app.infrastructure.database.sqlserver.repositories.sql_chemical_repository import SqlChemicalRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.qr.qr_code_service import QrCodeService

router = APIRouter(prefix="/batches", tags=["Batches"])


def create_batch_service(session) -> BatchService:
    return BatchService(
        SqlBatchRepository(session),
        QrCodeService(),
        SqlFarmRepository(session),
        SqlCropTypeRepository(session),
        batch_chemical_repository=SqlBatchChemicalRepository(session),
        chemical_repository=SqlChemicalRepository(session),
    )


@router.post("/")
async def create_batch(
    request: CreateBatchRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        return await create_batch_service(session).create_batch(request)


@router.get("/")
async def list_batches(
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        return await create_batch_service(session).list_batches()


@router.get("/{batch_id}")
async def get_batch(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Lấy chi tiết batch kèm danh sách hóa chất đã sử dụng — mọi role đều xem được."""
    async with get_async_session() as session:
        service = create_batch_service(session)
        batch = await service.get_by_id(batch_id)
        chemicals = await service.get_batch_chemicals(batch_id)
        return BatchDetailResponse(
            id=batch.id,
            farm_id=batch.farm_id,
            crop_type_id=batch.crop_type_id,
            product_name=batch.product_name,
            harvest_date=batch.harvest_date,
            quantity=batch.quantity,
            quantity_unit=batch.quantity_unit,
            grade=batch.grade,
            status=int(batch.status),
            risk_level=int(batch.risk_level),
            qr_code_url=batch.qr_code_url,
            chemicals=[
                BatchChemicalSummary(chemical_id=c.chemical_id, applied_at=c.applied_at)
                for c in chemicals
            ],
        )


@router.put("/{batch_id}")
async def update_batch(
    batch_id: str,
    request: UpdateBatchRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        return await create_batch_service(session).update_batch(batch_id, request)


@router.delete("/{batch_id}")
async def delete_batch(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        return await create_batch_service(session).delete_batch(batch_id)


@router.post("/{batch_id}/qr")
async def regenerate_batch_qr(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        return await create_batch_service(session).regenerate_qr_code(batch_id)


@router.get("/{batch_id}/qr-image")
async def get_batch_qr_image(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        batch = await create_batch_service(session).regenerate_qr_code(batch_id)
        return FileResponse(batch.qr_code_url, media_type="image/png")


# ──────────── Hóa chất của lô ────────────

@router.put("/{batch_id}/chemicals")
async def set_batch_chemicals(
    batch_id: str,
    items: List[BatchChemicalItem],
    current_user: dict = Depends(require_roles(RoleName.FARMER)),
):
    """Nông dân cập nhật danh sách hóa chất đã dùng cho lô — chỉ FARMER."""
    async with get_async_session() as session:
        result = await create_batch_service(session).set_batch_chemicals(batch_id, items)
        return [BatchChemicalResponse(chemical_id=r.chemical_id, applied_at=r.applied_at) for r in result]


@router.get("/{batch_id}/chemicals")
async def get_batch_chemicals(
    batch_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Xem danh sách hóa chất đã dùng cho lô — mọi role đều xem được."""
    async with get_async_session() as session:
        result = await create_batch_service(session).get_batch_chemicals(batch_id)
        return [BatchChemicalResponse(chemical_id=r.chemical_id, applied_at=r.applied_at) for r in result]

