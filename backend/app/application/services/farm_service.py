import uuid

from app.domain.interfaces.repositories.farm_repository import FarmRepository
from app.domain.entities.farm import Farm
from app.domain.interfaces.repositories.user_repository import UserRepository


class FarmService:

    def __init__(
        self,
        farm_repository: FarmRepository,
        user_repository: UserRepository | None = None,
    ):
        self.farm_repository = farm_repository
        self.user_repository = user_repository

    async def create_farm(self, data):
        await self._validate_farm_data(data)
        farm = Farm(
            id=data.id or str(uuid.uuid4()),
            owner_id=data.owner_id,
            name=data.name,
            address=data.address,
            planting_date=data.planting_date,
            harvest_date=data.harvest_date,
        )
        return await self.farm_repository.save(farm)

    async def list_farms(self):
        return await self.farm_repository.find_all()

    async def update_farm(self, farm_id: str, data):
        existing_farm = await self.get_by_id(farm_id)
        await self._validate_farm_data(data)
        farm = Farm(
            id=existing_farm.id,
            owner_id=data.owner_id,
            name=data.name,
            address=data.address,
            planting_date=data.planting_date,
            harvest_date=data.harvest_date,
        )
        return await self.farm_repository.update(farm)

    async def delete_farm(self, farm_id: str):
        await self.get_by_id(farm_id)
        await self.farm_repository.delete(farm_id)
        return {"message": "Farm deleted successfully"}

    async def _validate_farm_data(self, data) -> None:
        await self._validate_owner(data.owner_id)
        self._validate_required_text(data.name, "Farm name")
        self._validate_required_text(data.address, "Farm address")
        if data.planting_date and data.harvest_date and data.harvest_date < data.planting_date:
            raise ValueError("Farm harvest_date must be after planting_date")

    async def _validate_owner(self, owner_id: str) -> None:
        if self.user_repository is None:
            return
        owner = await self.user_repository.find_by_id(owner_id)
        if owner is None:
            raise ValueError("Farm owner_id does not exist")

    def _validate_required_text(self, value: str | None, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")

    async def get_by_id(self, farm_id: str):
        farm = await self.farm_repository.find_by_id(farm_id)
        if farm is None:
            raise ValueError("Farm not found")
        return farm
