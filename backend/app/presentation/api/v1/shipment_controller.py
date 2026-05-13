from fastapi import APIRouter
from app.application.dto.shipment_dto import CreateShipmentRequest
from app.application.services.shipment_service import ShipmentService
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/")
async def create_shipment(request: CreateShipmentRequest):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session))
        return await shipment_service.create_shipment(request)
