from fastapi import APIRouter, Depends

from app.application.dto.container_dto import CreateContainerRequest, UpdateContainerRequest
from app.application.services.container_service import ContainerService
from app.core.dependencies import get_current_user
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/containers", tags=["Containers"])


@router.post("/")
async def create_container(
    request: CreateContainerRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.create_container(request)


@router.get("/")
async def list_containers(
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.list_containers()


@router.get("/{container_id}")
async def get_container(
    container_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.get_by_id(container_id)


@router.put("/{container_id}")
async def update_container(
    container_id: str,
    request: UpdateContainerRequest,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session))
        return await container_service.update_container(container_id, request)


@router.delete("/{container_id}")
async def delete_container(
    container_id: str,
    current_user: dict = Depends(get_current_user),
):
    async with get_async_session() as session:
        container_service = ContainerService(SqlContainerRepository(session), SqlShipmentRepository(session))
        return await container_service.delete_container(container_id)
