from fastapi import APIRouter, Depends

from app.application.facades.traceability_facade import TraceabilityFacade
from app.core.dependencies import get_traceability_facade, require_roles
from app.domain.enums.role import RoleName

router = APIRouter(prefix="/traceability", tags=["Traceability"])


@router.get("/{batch_id}")
async def trace_batch(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
    current_user: dict = Depends(
        require_roles(
            RoleName.ADMIN,
            RoleName.FARMER,
            RoleName.TRADER,
            RoleName.DISTRIBUTOR,
        )
    ),
):
    """Xem đầy đủ thông tin truy xuất nguồn gốc — yêu cầu đăng nhập."""
    return await traceability.trace_batch(batch_id)


@router.get("/{batch_id}/public")
async def trace_batch_public(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
):
    """Endpoint công khai dành cho người tiêu dùng quét QR code."""
    return await traceability.trace_batch_public(batch_id)
