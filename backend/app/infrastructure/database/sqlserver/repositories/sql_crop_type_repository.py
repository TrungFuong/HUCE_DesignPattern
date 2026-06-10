from sqlalchemy import select

from app.domain.entities.crop_type import CropType
from app.domain.interfaces.repositories.crop_type_repository import CropTypeRepository
from app.infrastructure.database.sqlserver.models.crop_type_model import CropTypeModel


class SqlCropTypeRepository(CropTypeRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def _to_entity(self, model: CropTypeModel) -> CropType:
        return CropType(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
        )

    async def find_by_id(self, crop_type_id: str) -> CropType | None:
        model = await self.db_session.get(CropTypeModel, crop_type_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_code(self, code: str) -> CropType | None:
        result = await self.db_session.execute(select(CropTypeModel).where(CropTypeModel.code == code))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all(self) -> list[CropType]:
        result = await self.db_session.execute(select(CropTypeModel).order_by(CropTypeModel.code.asc()))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def save(self, crop_type: CropType) -> CropType:
        model = CropTypeModel(
            id=crop_type.id,
            code=crop_type.code,
            name=crop_type.name,
            description=crop_type.description,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return crop_type

    async def update(self, crop_type: CropType) -> CropType:
        model = await self.db_session.get(CropTypeModel, crop_type.id)
        if model is None:
            raise ValueError("Crop type not found")
        model.code = crop_type.code
        model.name = crop_type.name
        model.description = crop_type.description
        await self.db_session.commit()
        return crop_type

    async def delete(self, crop_type_id: str) -> None:
        model = await self.db_session.get(CropTypeModel, crop_type_id)
        if model is None:
            raise ValueError("Crop type not found")
        await self.db_session.delete(model)
        await self.db_session.commit()
