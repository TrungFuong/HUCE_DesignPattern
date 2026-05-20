import uuid

from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.domain.entities.batch import Batch
from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel
from app.domain.interfaces.repositories.crop_type_repository import CropTypeRepository
from app.domain.interfaces.repositories.farm_repository import FarmRepository
from app.domain.interfaces.services.qr_service import QrService


class BatchService:

    def __init__(
        self,
        batch_repository: BatchRepository,
        qr_service: QrService,
        farm_repository: FarmRepository | None = None,
        crop_type_repository: CropTypeRepository | None = None,
    ):
        self.batch_repository = batch_repository
        self.qr_service = qr_service
        self.farm_repository = farm_repository
        self.crop_type_repository = crop_type_repository

    async def create_batch(self, data):
        await self._validate_farm(data.farm_id)
        crop_type_id = data.crop_type_id
        self._validate_required_text(crop_type_id, "Crop type id")
        await self._validate_crop_type_id(crop_type_id)
        self._validate_required_text(data.product_name, "Product name")
        self._validate_positive_quantity(data.quantity, "Batch quantity")
        self._validate_required_text(data.quantity_unit, "Batch quantity unit")
        batch = Batch(
            id=data.id or str(uuid.uuid4()),
            farm_id=data.farm_id,
            crop_type_id=crop_type_id.strip(),
            product_name=data.product_name,
            harvest_date=data.harvest_date,
            quantity=data.quantity,
            quantity_unit=data.quantity_unit,
            grade=data.grade,
            status=BatchStatus.CREATED,
            risk_level=RiskLevel.NORMAL,
        )
        saved_batch = await self.batch_repository.save(batch)
        qr_url = await self.qr_service.generate_for_batch(saved_batch.id)
        saved_batch.qr_code_url = qr_url
        return await self.batch_repository.update(saved_batch)

    async def _validate_farm(self, farm_id: str) -> None:
        if self.farm_repository is None:
            return None
        farm = await self.farm_repository.find_by_id(farm_id)
        if farm is None:
            raise ValueError("Batch farm_id does not exist")
        return farm

    async def _validate_crop_type_id(self, crop_type_id: str) -> None:
        if self.crop_type_repository is None:
            return
        crop_type = await self.crop_type_repository.find_by_id(crop_type_id.strip())
        if crop_type is None:
            raise ValueError("Batch crop_type_id does not exist")

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")

    def _validate_positive_quantity(self, value: float, field_name: str) -> None:
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")

    async def get_by_id(self, batch_id: str):
        batch = await self.batch_repository.find_by_id(batch_id)
        if batch is None:
            raise ValueError("Batch not found")
        return batch

    async def mark_batch_at_risk(self, batch_id: str):
        batch = await self.get_by_id(batch_id)
        batch.mark_at_risk()
        return await self.batch_repository.update(batch)

    async def regenerate_qr_code(self, batch_id: str):
        batch = await self.get_by_id(batch_id)
        batch.qr_code_url = await self.qr_service.generate_for_batch(batch.id)
        return await self.batch_repository.update(batch)
