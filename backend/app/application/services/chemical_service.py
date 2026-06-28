import uuid

from app.application.dto.chemical_dto import ChemicalRequest
from app.domain.entities.chemical import Chemical
from app.domain.interfaces.repositories.chemical_repository import ChemicalRepository
from app.domain.interfaces.repositories.crop_type_repository import CropTypeRepository


class ChemicalService:

    def __init__(
        self,
        chemical_repository: ChemicalRepository,
        crop_type_repository: CropTypeRepository,
    ):
        self.chemical_repository = chemical_repository
        self.crop_type_repository = crop_type_repository

    async def create_chemical(self, data: ChemicalRequest) -> Chemical:
        self._validate_required_text(data.name, "Tên hóa chất")
        self._validate_required_text(data.unit, "Đơn vị")
        crop_type = await self.crop_type_repository.find_by_id(data.crop_type_id)
        if crop_type is None:
            raise ValueError("Loại nông sản không tồn tại")
        return await self.chemical_repository.save(
            Chemical(
                id=str(uuid.uuid4()),
                crop_type_id=data.crop_type_id,
                name=data.name.strip(),
                unit=data.unit.strip(),
                description=data.description,
            )
        )

    async def list_all(self) -> list[Chemical]:
        return await self.chemical_repository.find_all()

    async def list_by_crop_type(self, crop_type_id: str) -> list[Chemical]:
        crop_type = await self.crop_type_repository.find_by_id(crop_type_id)
        if crop_type is None:
            raise ValueError("Loại nông sản không tồn tại")
        return await self.chemical_repository.find_by_crop_type_id(crop_type_id)

    async def update_chemical(self, chemical_id: str, data: ChemicalRequest) -> Chemical:
        existing = await self._get_or_raise(chemical_id)
        self._validate_required_text(data.name, "Tên hóa chất")
        self._validate_required_text(data.unit, "Đơn vị")
        crop_type = await self.crop_type_repository.find_by_id(data.crop_type_id)
        if crop_type is None:
            raise ValueError("Loại nông sản không tồn tại")
        return await self.chemical_repository.update(
            Chemical(
                id=existing.id,
                crop_type_id=data.crop_type_id,
                name=data.name.strip(),
                unit=data.unit.strip(),
                description=data.description,
            )
        )

    async def delete_chemical(self, chemical_id: str) -> dict:
        await self._get_or_raise(chemical_id)
        if await self.chemical_repository.is_used_by_batch(chemical_id):
            raise ValueError("Không thể xóa hóa chất đang được sử dụng bởi lô nông sản")
        await self.chemical_repository.soft_delete(chemical_id)
        return {"message": "Xóa hóa chất thành công"}

    async def _get_or_raise(self, chemical_id: str) -> Chemical:
        chemical = await self.chemical_repository.find_by_id(chemical_id)
        if chemical is None:
            raise ValueError("Hóa chất không tồn tại")
        return chemical

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} không được để trống")
