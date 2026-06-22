from fastapi import APIRouter, Depends

from app.application.dto.container_dto import CreateContainerRequest, UpdateContainerRequest
from app.application.services.container_service import ContainerService
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName

router = APIRouter(
    prefix="/containers",
    tags=["Containers"],
    dependencies=[Depends(require_roles(RoleName.ADMIN, RoleName.TRADER))],
)


@router.post("/")
async def create_container(request: CreateContainerRequest):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.create_container(request)


@router.get("/")
async def list_containers():
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.list_containers()


@router.get("/{container_id}")
async def get_container(container_id: str):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.get_by_id(container_id)


@router.put("/{container_id}")
async def update_container(container_id: str, request: UpdateContainerRequest):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.update_container(container_id, request)


@router.delete("/{container_id}")
async def delete_container(container_id: str):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session), SqlShipmentRepository(session))
        return await container_service.delete_container(container_id)
