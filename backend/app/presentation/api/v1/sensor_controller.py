from fastapi import APIRouter, Depends
from app.application.dto.sensor_log_dto import SensorLogRequest
from app.application.services.sensor_service import SensorService
from app.infrastructure.database.mongodb.mongo_client import get_mongo_database
from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
from app.core.dependencies import require_roles
from app.domain.enums.role import RoleName

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"],
    dependencies=[Depends(require_roles(RoleName.ADMIN))],
)


@router.post("/")
async def save_sensor_log(request: SensorLogRequest):
    sensor_service = SensorService(MongoSensorLogRepository(get_mongo_database()))
    return await sensor_service.save_sensor_log(request)
