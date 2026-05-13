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
        return Farm(
            id=model.id,
            owner_id=model.owner_id,
            name=model.name,
            address=model.address,
            crop_type=model.crop_type,
            planting_date=model.planting_date,
            harvest_date=model.harvest_date,
        )

    async def save(self, farm: Farm) -> Farm:
        model = FarmModel(
            id=farm.id,
            owner_id=farm.owner_id,
            name=farm.name,
            address=farm.address,
            crop_type=farm.crop_type,
            planting_date=farm.planting_date,
            harvest_date=farm.harvest_date,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return farm
