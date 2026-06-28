import uuid

from app.application.dto.crop_type_dto import CropTypeRequest
from app.domain.entities.crop_type import CropType
from app.domain.interfaces.repositories.crop_type_repository import CropTypeRepository


class CropTypeService:

    def __init__(self, crop_type_repository: CropTypeRepository):
        self.crop_type_repository = crop_type_repository

    async def create_crop_type(self, data: CropTypeRequest) -> CropType:
        code = self._normalize_code(data.code)
        self._validate_required_text(data.name, "Crop type name")
        existing = await self.crop_type_repository.find_by_code(code)
        if existing:
            raise ValueError("Crop type already exists")
        return await self.crop_type_repository.save(
            CropType(
                id=str(uuid.uuid4()),
                code=code,
                name=data.name,
                description=data.description,
            )
        )

    async def get_by_code(self, code: str) -> CropType:
        crop_type = await self.crop_type_repository.find_by_code(self._normalize_code(code))
        if crop_type is None:
            raise ValueError("Crop type not found")
        return crop_type

    async def list_crop_types(self) -> list[CropType]:
        return await self.crop_type_repository.find_all()

    async def update_crop_type(self, crop_type_id: str, data: CropTypeRequest) -> CropType:
        existing_crop_type = await self.get_by_id(crop_type_id)
        code = self._normalize_code(data.code)
        self._validate_required_text(data.name, "Crop type name")
        existing_code = await self.crop_type_repository.find_by_code(code)
        if existing_code and existing_code.id != existing_crop_type.id:
            raise ValueError("Crop type already exists")
        return await self.crop_type_repository.update(
            CropType(
                id=existing_crop_type.id,
                code=code,
                name=data.name,
                description=data.description,
            )
        )

    async def delete_crop_type(self, crop_type_id: str):
        await self.get_by_id(crop_type_id)
        await self.crop_type_repository.delete(crop_type_id)
        return {"message": "Crop type deleted successfully"}

    async def get_by_id(self, crop_type_id: str) -> CropType:
        crop_type = await self.crop_type_repository.find_by_id(crop_type_id)
        if crop_type is None:
            raise ValueError("Crop type not found")
        return crop_type

    def _normalize_code(self, code: str) -> str:
        self._validate_required_text(code, "Crop type code")
        return code.strip().upper()

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")
