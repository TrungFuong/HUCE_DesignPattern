from sqlalchemy import select

from app.application.utils.enum_parser import parse_enum
from app.domain.entities.batch import Batch
from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel
from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.infrastructure.database.sqlserver.models.batch_model import BatchModel
from app.infrastructure.database.sqlserver.models.farm_model import FarmModel


class SqlBatchRepository(BatchRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_by_id(self, batch_id: str) -> Batch | None:
        model = await self.db_session.get(BatchModel, batch_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all(self) -> list[Batch]:
        result = await self.db_session.execute(select(BatchModel).order_by(BatchModel.harvest_date.desc()))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def save(self, batch: Batch) -> Batch:
        model = BatchModel(
            id=batch.id,
            farm_id=batch.farm_id,
            crop_type_id=batch.crop_type_id,
            product_name=batch.product_name,
            harvest_date=batch.harvest_date,
            quantity=batch.quantity,
            quantity_unit=batch.quantity_unit,
            grade=batch.grade,
            status=int(batch.status),
            risk_level=int(batch.risk_level),
            qr_code_url=batch.qr_code_url,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return batch

    async def update(self, batch: Batch) -> Batch:
        model = await self.db_session.get(BatchModel, batch.id)
        if model is None:
            return await self.save(batch)
        model.farm_id = batch.farm_id
        model.crop_type_id = batch.crop_type_id
        model.product_name = batch.product_name
        model.harvest_date = batch.harvest_date
        model.quantity = batch.quantity
        model.quantity_unit = batch.quantity_unit
        model.grade = batch.grade
        model.status = int(batch.status)
        model.risk_level = int(batch.risk_level)
        model.qr_code_url = batch.qr_code_url
        await self.db_session.commit()
        return batch

    async def delete(self, batch_id: str) -> None:
        model = await self.db_session.get(BatchModel, batch_id)
        if model is None:
            raise ValueError("Batch not found")
        await self.db_session.delete(model)
        await self.db_session.commit()

    async def find_by_farm_id(self, farm_id: str) -> list[Batch]:
        result = await self.db_session.execute(select(BatchModel).where(BatchModel.farm_id == farm_id))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def find_by_owner_id(self, owner_id: str) -> list[Batch]:
        result = await self.db_session.execute(
            select(BatchModel)
            .join(FarmModel, BatchModel.farm_id == FarmModel.id)
            .where(FarmModel.owner_id == owner_id)
            .order_by(BatchModel.harvest_date.desc())
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def find_by_crop_type_id(self, crop_type_id: str) -> list[Batch]:
        result = await self.db_session.execute(
            select(BatchModel)
            .where(BatchModel.crop_type_id == crop_type_id)
            .order_by(BatchModel.harvest_date.desc())
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    def _to_entity(self, model: BatchModel) -> Batch:
        return Batch(
            id=model.id,
            farm_id=model.farm_id,
            crop_type_id=model.crop_type_id,
            product_name=model.product_name,
            harvest_date=model.harvest_date,
            quantity=model.quantity,
            quantity_unit=model.quantity_unit,
            grade=model.grade,
            status=parse_enum(BatchStatus, model.status),
            risk_level=parse_enum(RiskLevel, model.risk_level),
            qr_code_url=model.qr_code_url,
        )
