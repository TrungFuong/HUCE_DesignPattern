from fastapi import APIRouter
from app.application.dto.batch_dto import CreateBatchRequest
from app.application.services.batch_service import BatchService
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.qr.qr_code_service import QrCodeService

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("/")
async def create_batch(request: CreateBatchRequest):
    async with get_async_session() as session:
        batch_service = BatchService(SqlBatchRepository(session), QrCodeService())
        return await batch_service.create_batch(request)


@router.get("/{batch_id}")
async def get_batch(batch_id: str):
    async with get_async_session() as session:
        batch_service = BatchService(SqlBatchRepository(session), QrCodeService())
        return await batch_service.get_by_id(batch_id)
