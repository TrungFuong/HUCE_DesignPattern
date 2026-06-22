from fastapi import APIRouter, Depends

from app.application.facades.traceability_facade import TraceabilityFacade
from app.core.dependencies import get_traceability_facade
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName

router = APIRouter(prefix="/traceability", tags=["Traceability"])


@router.get("/{batch_id}")
async def trace_batch(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
    _=Depends(require_roles(RoleName.ADMIN, RoleName.FARMER, RoleName.TRADER, RoleName.DISTRIBUTOR)),
):
    return await traceability.trace_batch(batch_id)


@router.get("/{batch_id}/public")
async def trace_batch_public(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
):
    return await traceability.trace_batch_public(batch_id)
