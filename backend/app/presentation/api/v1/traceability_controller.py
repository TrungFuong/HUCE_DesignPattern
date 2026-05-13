from fastapi import APIRouter, Depends

from app.application.facades.traceability_facade import TraceabilityFacade
from app.core.dependencies import get_traceability_facade

router = APIRouter(prefix="/traceability", tags=["Traceability"])


@router.get("/{batch_id}")
async def trace_batch(
    batch_id: str,
    traceability: TraceabilityFacade = Depends(get_traceability_facade),
):
    return await traceability.trace_batch(batch_id)
