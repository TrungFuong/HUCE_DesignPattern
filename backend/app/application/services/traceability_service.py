from app.application.facades.traceability_facade import TraceabilityFacade


class TraceabilityService:

    def __init__(self, traceability_facade: TraceabilityFacade):
        self.traceability_facade = traceability_facade

    async def trace_batch(self, batch_id: str):
        return await self.traceability_facade.trace_batch(batch_id)
