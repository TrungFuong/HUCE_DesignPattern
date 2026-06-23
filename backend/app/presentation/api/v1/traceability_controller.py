from fastapi import APIRouter, Depends

from app.application.facades.traceability_facade import TraceabilityFacade
from app.core.dependencies import get_current_user, get_traceability_facade

router = APIRouter(prefix="/traceability", tags=["Traceability"])


@router.get("/{batch_id}")
async def trace_batch(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
    current_user: dict = Depends(get_current_user),
):
    """Xem đầy đủ thông tin truy xuất nguồn gốc — yêu cầu đăng nhập."""
    return await traceability.trace_batch(batch_id)


@router.get("/{batch_id}/public")
async def trace_batch_public(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
):
    """
    Endpoint công khai dành cho người tiêu dùng quét QR code.
    Không yêu cầu đăng nhập — trả về thông tin rút gọn.
    """
    return await traceability.trace_batch_public(batch_id)
