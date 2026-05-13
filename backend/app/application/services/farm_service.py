import uuid

from app.domain.interfaces.repositories.farm_repository import FarmRepository
from app.domain.entities.farm import Farm


class FarmService:

    def __init__(self, farm_repository: FarmRepository):
        self.farm_repository = farm_repository

    async def create_farm(self, data):
        farm = Farm(
            id=data.id or str(uuid.uuid4()),
            owner_id=data.owner_id,
            name=data.name,
            address=data.address,
            crop_type=data.crop_type,
            planting_date=data.planting_date,
            harvest_date=data.harvest_date,
        )
        return await self.farm_repository.save(farm)

    async def get_by_id(self, farm_id: str):
        farm = await self.farm_repository.find_by_id(farm_id)
        if farm is None:
            raise ValueError("Farm not found")
        return farm
