from sqlalchemy import select

from app.domain.entities.farm import Farm
from app.domain.interfaces.repositories.farm_repository import FarmRepository
from app.infrastructure.database.sqlserver.models.farm_model import FarmModel


class SqlFarmRepository(FarmRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def find_by_id(self, farm_id: str) -> Farm | None:
        model = await self.db_session.get(FarmModel, farm_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all(self) -> list[Farm]:
        result = await self.db_session.execute(select(FarmModel).order_by(FarmModel.name))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def save(self, farm: Farm) -> Farm:
        model = FarmModel(
            id=farm.id,
            owner_id=farm.owner_id,
            name=farm.name,
            address=farm.address,
            planting_date=farm.planting_date,
            harvest_date=farm.harvest_date,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return farm

    async def update(self, farm: Farm) -> Farm:
        model = await self.db_session.get(FarmModel, farm.id)
        if model is None:
            raise ValueError("Farm not found")
        model.owner_id = farm.owner_id
        model.name = farm.name
        model.address = farm.address
        model.planting_date = farm.planting_date
        model.harvest_date = farm.harvest_date
        await self.db_session.commit()
        return farm

    async def delete(self, farm_id: str) -> None:
        model = await self.db_session.get(FarmModel, farm_id)
        if model is None:
            raise ValueError("Farm not found")
        await self.db_session.delete(model)
        await self.db_session.commit()

    def _to_entity(self, model: FarmModel) -> Farm:
        return Farm(
            id=model.id,
            owner_id=model.owner_id,
            name=model.name,
            address=model.address,
            planting_date=model.planting_date,
            harvest_date=model.harvest_date,
        )
