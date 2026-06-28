from sqlalchemy import select

from app.domain.entities.batch_chemical import BatchChemical
from app.domain.interfaces.repositories.batch_chemical_repository import BatchChemicalRepository
from app.infrastructure.database.sqlserver.models.batch_chemical_model import BatchChemicalModel


class SqlBatchChemicalRepository(BatchChemicalRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def _to_entity(self, model: BatchChemicalModel) -> BatchChemical:
        return BatchChemical(
            batch_id=model.batch_id,
            chemical_id=model.chemical_id,
            applied_at=model.applied_at,
        )

    async def find_by_batch_id(self, batch_id: str) -> list[BatchChemical]:
        result = await self.db_session.execute(
            select(BatchChemicalModel).where(
                BatchChemicalModel.batch_id == batch_id,
                BatchChemicalModel.is_deleted == False,  # noqa: E712
            )
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def save_all(self, items: list[BatchChemical]) -> list[BatchChemical]:
        for item in items:
            existing = await self.db_session.get(
                BatchChemicalModel, (item.batch_id, item.chemical_id)
            )
            if existing:
                existing.is_deleted = False
                existing.applied_at = item.applied_at
            else:
                model = BatchChemicalModel(
                    batch_id=item.batch_id,
                    chemical_id=item.chemical_id,
                    applied_at=item.applied_at,
                    is_deleted=False,
                )
                self.db_session.add(model)
        await self.db_session.commit()
        return items

    async def delete_by_batch_id(self, batch_id: str) -> None:
        result = await self.db_session.execute(
            select(BatchChemicalModel).where(
                BatchChemicalModel.batch_id == batch_id,
                BatchChemicalModel.is_deleted == False,  # noqa: E712
            )
        )
        for model in result.scalars().all():
            model.is_deleted = True
        await self.db_session.commit()
