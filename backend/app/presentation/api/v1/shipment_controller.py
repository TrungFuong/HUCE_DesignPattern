from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import require_roles
from app.domain.entities.user import User
from app.domain.enums.role import RoleName
from app.application.dto.shipment_dto import CreateShipmentRequest
from app.application.services.shipment_service import ShipmentService
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/")
async def create_shipment(
    request: CreateShipmentRequest,
    _=Depends(require_roles(RoleName.ADMIN, RoleName.TRADER)),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            SqlUserRepository(session),
            SqlContainerRepository(session),
        )
        return await shipment_service.create_shipment(request)


@router.get("/")
async def list_shipments(
    current_user: User = Depends(
        require_roles(RoleName.ADMIN, RoleName.TRADER, RoleName.DISTRIBUTOR)
    ),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            container_repository=SqlContainerRepository(session),
        )
        if current_user.role == RoleName.DISTRIBUTOR:
            return await shipment_service.list_shipments_for_distributor(current_user.id)
        return await shipment_service.list_shipments()


@router.get("/{shipment_id}")
async def get_shipment(
    shipment_id: str,
    current_user: User = Depends(
        require_roles(RoleName.ADMIN, RoleName.TRADER, RoleName.DISTRIBUTOR)
    ),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            container_repository=SqlContainerRepository(session),
        )
        shipment = await shipment_service.get_by_id(shipment_id)
        if current_user.role == RoleName.DISTRIBUTOR and shipment.to_actor_id != current_user.id:
            raise HTTPException(status_code=403, detail="Bạn chỉ có thể xem chuyến vận chuyển gửi đến mình")
        return await shipment_service.get_with_items(shipment_id)


@router.put("/{shipment_id}")
async def update_shipment(
    shipment_id: str,
    request: CreateShipmentRequest,
    _=Depends(require_roles(RoleName.ADMIN, RoleName.TRADER)),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(
            SqlShipmentRepository(session),
            SqlBatchRepository(session),
            SqlUserRepository(session),
            SqlContainerRepository(session),
        )
        return await shipment_service.update_shipment(shipment_id, request)


@router.delete("/{shipment_id}")
async def delete_shipment(
    shipment_id: str,
    _=Depends(require_roles(RoleName.ADMIN, RoleName.TRADER)),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.delete_shipment(shipment_id)


@router.get("/batch/{batch_id}")
async def get_shipments_by_batch(
    batch_id: str,
    _=Depends(require_roles(RoleName.ADMIN, RoleName.TRADER)),
):
    async with get_async_session() as session:
        shipment_service = ShipmentService(SqlShipmentRepository(session), SqlBatchRepository(session))
        return await shipment_service.get_by_batch_id(batch_id)
