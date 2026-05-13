from sqlalchemy import select

from app.domain.entities.batch import Batch
from app.domain.interfaces.repositories.batch_repository import BatchRepository
from app.infrastructure.database.sqlserver.models.batch_model import BatchModel


class SqlBatchRepository(BatchRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_by_id(self, batch_id: str) -> Batch | None:
        model = await self.db_session.get(BatchModel, batch_id)
        if model is None:
            return None
        return Batch(
            id=model.id,
            farm_id=model.farm_id,
            product_name=model.product_name,
            harvest_date=model.harvest_date,
            status=model.status,
            risk_level=model.risk_level,
            qr_code_url=model.qr_code_url,
        )

    async def save(self, batch: Batch) -> Batch:
        model = BatchModel(
            id=batch.id,
            farm_id=batch.farm_id,
            product_name=batch.product_name,
            harvest_date=batch.harvest_date,
            status=batch.status,
            risk_level=batch.risk_level,
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
        model.product_name = batch.product_name
        model.harvest_date = batch.harvest_date
        model.status = batch.status
        model.risk_level = batch.risk_level
        model.qr_code_url = batch.qr_code_url
        await self.db_session.commit()
        return batch

    async def find_by_farm_id(self, farm_id: str) -> list[Batch]:
        result = await self.db_session.execute(select(BatchModel).where(BatchModel.farm_id == farm_id))
        return [
            Batch(
                id=model.id,
                farm_id=model.farm_id,
                product_name=model.product_name,
                harvest_date=model.harvest_date,
                status=model.status,
                risk_level=model.risk_level,
                qr_code_url=model.qr_code_url,
            )
            for model in result.scalars().all()
        ]
