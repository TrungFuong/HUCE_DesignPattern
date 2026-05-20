from sqlalchemy import select

from app.domain.entities.container import Container
from app.domain.enums.container_status import ContainerStatus
from app.domain.interfaces.repositories.container_repository import ContainerRepository
from app.infrastructure.database.sqlserver.models.container_model import ContainerModel


class SqlContainerRepository(ContainerRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def _to_entity(self, model: ContainerModel) -> Container:
        return Container(
            id=model.id,
            code=model.code,
            type=model.type,
            capacity=model.capacity,
            capacity_unit=model.capacity_unit,
            material=model.material,
            is_temperature_controlled=model.is_temperature_controlled,
            min_temperature=model.min_temperature,
            max_temperature=model.max_temperature,
            status=ContainerStatus(model.status),
            description=model.description,
        )

    async def find_by_id(self, container_id: str) -> Container | None:
        model = await self.db_session.get(ContainerModel, container_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_code(self, code: str) -> Container | None:
        result = await self.db_session.execute(select(ContainerModel).where(ContainerModel.code == code))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all(self) -> list[Container]:
        result = await self.db_session.execute(select(ContainerModel).order_by(ContainerModel.code.asc()))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def save(self, container: Container) -> Container:
        model = ContainerModel(
            id=container.id,
            code=container.code,
            type=container.type,
            capacity=container.capacity,
            capacity_unit=container.capacity_unit,
            material=container.material,
            is_temperature_controlled=container.is_temperature_controlled,
            min_temperature=container.min_temperature,
            max_temperature=container.max_temperature,
            status=int(container.status),
            description=container.description,
        )
        self.db_session.add(model)
        await self.db_session.commit()
        return container

    async def update(self, container: Container) -> Container:
        model = await self.db_session.get(ContainerModel, container.id)
        if model is None:
            return await self.save(container)
        model.code = container.code
        model.type = container.type
        model.capacity = container.capacity
        model.capacity_unit = container.capacity_unit
        model.material = container.material
        model.is_temperature_controlled = container.is_temperature_controlled
        model.min_temperature = container.min_temperature
        model.max_temperature = container.max_temperature
        model.status = int(container.status)
        model.description = container.description
        await self.db_session.commit()
        return container

    async def delete(self, container_id: str) -> bool:
        model = await self.db_session.get(ContainerModel, container_id)
        if model is None:
            return False
        await self.db_session.delete(model)
        await self.db_session.commit()
        return True
