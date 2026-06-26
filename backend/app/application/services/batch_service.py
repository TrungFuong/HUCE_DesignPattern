import uuid

from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.domain.entities.batch import Batch
from app.domain.entities.batch_chemical import BatchChemical
from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel
from app.domain.interfaces.repositories.crop_type_repository import CropTypeRepository
from app.domain.interfaces.repositories.farm_repository import FarmRepository
from app.domain.interfaces.services.qr_service import QrService
from app.domain.interfaces.repositories.shipment_repository import ShipmentRepository
from app.domain.interfaces.repositories.batch_chemical_repository import BatchChemicalRepository
from app.domain.interfaces.repositories.chemical_repository import ChemicalRepository


class BatchService:

    def __init__(
        self,
        batch_repository: BatchRepository,
        qr_service: QrService,
        farm_repository: FarmRepository | None = None,
        crop_type_repository: CropTypeRepository | None = None,
        shipment_repository: ShipmentRepository | None = None,
        batch_chemical_repository: BatchChemicalRepository | None = None,
        chemical_repository: ChemicalRepository | None = None,
    ):
        self.batch_repository = batch_repository
        self.qr_service = qr_service
        self.farm_repository = farm_repository
        self.crop_type_repository = crop_type_repository
        self.shipment_repository = shipment_repository
        self.batch_chemical_repository = batch_chemical_repository
        self.chemical_repository = chemical_repository

    async def create_batch(self, data):
        await self._validate_batch_data(data)
        crop_type_id = data.crop_type_id.strip() if data.crop_type_id else None
        batch = Batch(
            id=data.id or str(uuid.uuid4()),
            farm_id=data.farm_id,
            crop_type_id=crop_type_id,
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

    async def list_batches(self):
        return await self.batch_repository.find_all()

    async def update_batch(self, batch_id: str, data):
        existing_batch = await self.get_by_id(batch_id)
        await self._validate_batch_data(data)
        batch = Batch(
            id=existing_batch.id,
            farm_id=data.farm_id,
            crop_type_id=data.crop_type_id.strip() if data.crop_type_id else None,
            product_name=data.product_name,
            harvest_date=data.harvest_date,
            quantity=data.quantity,
            quantity_unit=data.quantity_unit,
            grade=data.grade,
            status=existing_batch.status,
            risk_level=existing_batch.risk_level,
            qr_code_url=await self.qr_service.generate_for_batch(existing_batch.id),
        )
        return await self.batch_repository.update(batch)

    async def delete_batch(self, batch_id: str):
        await self.get_by_id(batch_id)
        if self.shipment_repository and await self.shipment_repository.find_items_by_batch_id(batch_id):
            raise ValueError("Không thể xóa lô sản phẩm đang nằm trong vận chuyển")
        await self.batch_repository.delete(batch_id)
        return {"message": "Batch deleted successfully"}

    async def _validate_batch_data(self, data) -> None:
        await self._validate_farm(data.farm_id)
        if data.crop_type_id:
            await self._validate_crop_type_id(data.crop_type_id)
        self._validate_required_text(data.product_name, "Product name")
        self._validate_positive_quantity(data.quantity, "Batch quantity")
        self._validate_required_text(data.quantity_unit, "Batch quantity unit")

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

    async def set_batch_chemicals(self, batch_id: str, items: list) -> list[BatchChemical]:
        """Farmer cập nhật danh sách hóa chất cho lô (replace toàn bộ)."""
        if self.batch_chemical_repository is None:
            raise ValueError("BatchChemicalRepository không khả dụng")
        await self.get_by_id(batch_id)  # kiểm tra batch tồn tại
        # Kiểm tra từng chemical_id hợp lệ
        if self.chemical_repository:
            for item in items:
                chemical = await self.chemical_repository.find_by_id(item.chemical_id)
                if chemical is None:
                    raise ValueError(f"Hóa chất {item.chemical_id} không tồn tại")
        # Soft-delete toàn bộ cũ, sau đó upsert mới
        await self.batch_chemical_repository.delete_by_batch_id(batch_id)
        new_items = [
            BatchChemical(
                batch_id=batch_id,
                chemical_id=item.chemical_id,
                applied_at=item.applied_at,
            )
            for item in items
        ]
        return await self.batch_chemical_repository.save_all(new_items)

    async def get_batch_chemicals(self, batch_id: str) -> list[BatchChemical]:
        """Lấy danh sách hóa chất đã dùng cho lô."""
        await self.get_by_id(batch_id)  # kiểm tra batch tồn tại
        if self.batch_chemical_repository is None:
            return []
        return await self.batch_chemical_repository.find_by_batch_id(batch_id)
