from functools import lru_cache
from typing import AsyncGenerator, Callable

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_access_token
from app.infrastructure.blockchain.blockchain_proxy import BlockchainProxy
from app.infrastructure.blockchain.smart_contract_adapter import SmartContractAdapter
from app.infrastructure.blockchain.web3_client import Web3Client
from app.infrastructure.database.mongodb.mongo_client import get_mongo_database
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_crop_type_repository import SqlCropTypeRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.infrastructure.qr.qr_code_service import QrCodeService
from app.infrastructure.hashing.sha256_hash_service import Sha256HashService
from app.application.builders.trace_response_builder import TraceResponseBuilder
from app.application.facades.traceability_facade import TraceabilityFacade
from app.application.facades.iot_pipeline_facade import IoTPipelineFacade
from app.application.observers.blockchain_observer import BlockchainObserver
from app.application.observers.dashboard_observer import DashboardObserver
from app.application.observers.mongo_sensor_observer import MongoSensorObserver
from app.application.observers.risk_observer import RiskObserver
from app.application.services.batch_service import BatchService
from app.application.services.blockchain_service import BlockchainService
from app.application.services.container_service import ContainerService
from app.application.services.crop_type_service import CropTypeService
from app.application.services.farm_service import FarmService
from app.application.services.risk_service import RiskService
from app.application.services.sensor_service import SensorService
from app.application.services.shipment_service import ShipmentService
from app.application.services.user_service import UserService
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.domain.enums.role import RoleName


@lru_cache()
def get_settings() -> object:
    return settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session() as session:
        yield session


async def get_mongo_db():
    yield get_mongo_database()


async def get_redis():
    yield get_redis_client()


_http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_http_bearer),
    db_session: AsyncSession = Depends(get_db_session),
) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header required")
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as error:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from error

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await SqlUserRepository(db_session).find_by_email(email)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User account is unavailable")

    return {
        **payload,
        "id": user.id,
        "sub": user.email,
        "email": user.email,
        "full_name": user.full_name,
        "role": int(user.role),
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


def require_roles(*allowed_roles: RoleName | int) -> Callable:
    allowed_role_values = {int(role) for role in allowed_roles}

    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in allowed_role_values:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
        return current_user

    return role_checker


@lru_cache()
def get_hash_service() -> Sha256HashService:
    return Sha256HashService()


@lru_cache()
def get_qr_service() -> QrCodeService:
    return QrCodeService()


@lru_cache()
def get_blockchain_client() -> SmartContractAdapter:
    web3 = Web3Client(settings.blockchain_rpc_url)
    contract = web3.get_contract(settings.contract_address)
    return SmartContractAdapter(web3=web3, contract=contract)


@lru_cache()
def get_blockchain_proxy() -> BlockchainProxy:
    return BlockchainProxy(blockchain_client=get_blockchain_client(), cache_client=get_redis_client())


@lru_cache()
def get_blockchain_service() -> BlockchainService:
    return BlockchainService(blockchain_client=get_blockchain_proxy())


def get_batch_service(db_session: AsyncSession = Depends(get_db_session)) -> BatchService:
    return BatchService(
        batch_repository=SqlBatchRepository(db_session),
        qr_service=get_qr_service(),
        farm_repository=SqlFarmRepository(db_session),
        crop_type_repository=SqlCropTypeRepository(db_session),
        shipment_repository=SqlShipmentRepository(db_session),
    )


def get_farm_service(db_session: AsyncSession = Depends(get_db_session)) -> FarmService:
    return FarmService(
        farm_repository=SqlFarmRepository(db_session),
        user_repository=SqlUserRepository(db_session),
        batch_repository=SqlBatchRepository(db_session),
    )


def get_shipment_service(db_session: AsyncSession = Depends(get_db_session)) -> ShipmentService:
    return ShipmentService(
        shipment_repository=SqlShipmentRepository(db_session),
        batch_repository=SqlBatchRepository(db_session),
        user_repository=SqlUserRepository(db_session),
        container_repository=SqlContainerRepository(db_session),
    )


def get_container_service(db_session: AsyncSession = Depends(get_db_session)) -> ContainerService:
    return ContainerService(
        container_repository=SqlContainerRepository(db_session),
        shipment_repository=SqlShipmentRepository(db_session),
    )


def get_user_service(db_session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(user_repository=SqlUserRepository(db_session))


def get_sensor_service(mongo_db=Depends(get_mongo_db)) -> SensorService:
    return SensorService(sensor_log_repository=MongoSensorLogRepository(mongo_db))


def get_risk_service(db_session: AsyncSession = Depends(get_db_session)) -> RiskService:
    return RiskService(risk_rule_repository=SqlRiskRuleRepository(db_session))


def get_crop_type_service(db_session: AsyncSession = Depends(get_db_session)) -> CropTypeService:
    return CropTypeService(
        crop_type_repository=SqlCropTypeRepository(db_session),
        batch_repository=SqlBatchRepository(db_session),
        risk_rule_repository=SqlRiskRuleRepository(db_session),
    )


def get_traceability_facade(
    db_session: AsyncSession = Depends(get_db_session),
    mongo_db=Depends(get_mongo_db),
) -> TraceabilityFacade:
    return TraceabilityFacade(
        batch_service=get_batch_service(db_session),
        farm_service=get_farm_service(db_session),
        shipment_service=get_shipment_service(db_session),
        sensor_service=get_sensor_service(mongo_db),
        blockchain_service=get_blockchain_service(),
        hash_service=get_hash_service(),
        user_service=get_user_service(db_session),
        container_service=get_container_service(db_session),
        crop_type_service=get_crop_type_service(db_session),
        trace_response_builder=TraceResponseBuilder(),
    )


def get_iot_pipeline_facade(
    db_session: AsyncSession = Depends(get_db_session),
    mongo_db=Depends(get_mongo_db),
) -> IoTPipelineFacade:
    return IoTPipelineFacade(
        mongo_observer=MongoSensorObserver(MongoSensorLogRepository(mongo_db)),
        risk_observer=RiskObserver(
            get_risk_service(db_session),
            get_batch_service(db_session),
        ),
        blockchain_observer=BlockchainObserver(RedisQueueAdapter(get_redis_client())),
        dashboard_observer=DashboardObserver(),
    )
