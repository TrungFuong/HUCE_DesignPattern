from sqlalchemy import select

from app.domain.entities.chemical import Chemical
from app.domain.interfaces.repositories.chemical_repository import ChemicalRepository
from app.infrastructure.database.sqlserver.models.batch_chemical_model import BatchChemicalModel
from app.infrastructure.database.sqlserver.models.chemical_model import ChemicalModel


class SqlChemicalRepository(ChemicalRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def _to_entity(self, model: ChemicalModel) -> Chemical:
        return Chemical(
            id=model.id,
            crop_type_id=model.crop_type_id,
            name=model.name,
            unit=model.unit,
            description=model.description,
            is_deleted=model.is_deleted,
        )

    async def find_by_id(self, chemical_id: str) -> Chemical | None:
        result = await self.db_session.execute(
            select(ChemicalModel).where(
                ChemicalModel.id == chemical_id,
                ChemicalModel.is_deleted == False,  # noqa: E712
            )
        )
        model = result.scalars().first()
        return self._to_entity(model) if model else None

    async def find_by_crop_type_id(self, crop_type_id: str) -> list[Chemical]:
        result = await self.db_session.execute(
            select(ChemicalModel)
            .where(
                ChemicalModel.crop_type_id == crop_type_id,
                ChemicalModel.is_deleted == False,  # noqa: E712
            )
            .order_by(ChemicalModel.name.asc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def find_all(self) -> list[Chemical]:
        result = await self.db_session.execute(
            select(ChemicalModel)
            .where(ChemicalModel.is_deleted == False)  # noqa: E712
            .order_by(ChemicalModel.crop_type_id.asc(), ChemicalModel.name.asc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def save(self, chemical: Chemical) -> Chemical:
        model = ChemicalModel(
            id=chemical.id,
            crop_type_id=chemical.crop_type_id,
            name=chemical.name,
            unit=chemical.unit,
            description=chemical.description,
            is_deleted=False,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return chemical

    async def update(self, chemical: Chemical) -> Chemical:
        model = await self.db_session.get(ChemicalModel, chemical.id)
        if model is None:
            raise ValueError("Chemical not found")
        model.crop_type_id = chemical.crop_type_id
        model.name = chemical.name
        model.unit = chemical.unit
        model.description = chemical.description
        await self.db_session.commit()
        return chemical

    async def soft_delete(self, chemical_id: str) -> None:
        model = await self.db_session.get(ChemicalModel, chemical_id)
        if model is None or model.is_deleted:
            raise ValueError("Chemical not found")
        model.is_deleted = True
        await self.db_session.commit()

    async def is_used_by_batch(self, chemical_id: str) -> bool:
        result = await self.db_session.execute(
            select(BatchChemicalModel).where(
                BatchChemicalModel.chemical_id == chemical_id,
                BatchChemicalModel.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalars().first() is not None
