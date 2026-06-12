from fastapi import APIRouter
from app.application.dto.shipment_dto import CreateShipmentRequest
from app.application.services.shipment_service import ShipmentService
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/")
async def create_shipment(request: CreateShipmentRequest):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            SqlUserRepository(session),
            SqlContainerRepository(session),
        )
        return await shipment_service.create_shipment(request)


@router.get("/")
async def list_shipments():
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.list_shipments()


@router.get("/{shipment_id}")
async def get_shipment(shipment_id: str):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.get_with_items(shipment_id)


@router.put("/{shipment_id}")
async def update_shipment(shipment_id: str, request: CreateShipmentRequest):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            SqlUserRepository(session),
            SqlContainerRepository(session),
        )
        return await shipment_service.update_shipment(shipment_id, request)


@router.delete("/{shipment_id}")
async def delete_shipment(shipment_id: str):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.delete_shipment(shipment_id)


@router.get("/batch/{batch_id}")
async def get_shipments_by_batch(batch_id: str):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.get_by_batch_id(batch_id)
