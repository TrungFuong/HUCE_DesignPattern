import uuid

from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.domain.entities.batch import Batch
from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel
from app.domain.interfaces.services.qr_service import QrService


class BatchService:

    def __init__(self, batch_repository: BatchRepository, qr_service: QrService):
        self.batch_repository = batch_repository
        self.qr_service = qr_service

    async def create_batch(self, data):
        batch = Batch(
            id=data.id or str(uuid.uuid4()),
            farm_id=data.farm_id,
            product_name=data.product_name,
            harvest_date=data.harvest_date,
            status=BatchStatus.CREATED,
            risk_level=RiskLevel.NORMAL,
        )
        saved_batch = await self.batch_repository.save(batch)
        qr_url = await self.qr_service.generate_for_batch(saved_batch.id)
        saved_batch.qr_code_url = qr_url
        return await self.batch_repository.update(saved_batch)

    async def get_by_id(self, batch_id: str):
        batch = await self.batch_repository.find_by_id(batch_id)
        if batch is None:
            raise ValueError("Batch not found")
        return batch

    async def mark_batch_at_risk(self, batch_id: str):
        batch = await self.get_by_id(batch_id)
        batch.mark_at_risk()
        return await self.batch_repository.update(batch)
