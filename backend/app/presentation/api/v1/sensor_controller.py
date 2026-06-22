from fastapi import APIRouter, Depends

from app.application.services.sensor_service import SensorService
from app.application.dto.sensor_log_dto import SensorLogRequest
from app.core.dependencies import get_sensor_service, get_current_user

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/")
async def save_sensor_log(
    request: SensorLogRequest,
    sensor_service: SensorService = Depends(get_sensor_service),
):
    """Lưu sensor log thủ công (thường dùng cho test, luồng thật qua MQTT)."""
    return await sensor_service.save_sensor_log(request)


@router.get("/{batch_id}")
async def get_sensor_logs(
    batch_id: str,
    sensor_service: SensorService = Depends(get_sensor_service),
    current_user: dict = Depends(get_current_user),
):
    """Lấy toàn bộ sensor logs của một batch."""
    logs = await sensor_service.get_logs_by_batch_id(batch_id)
    return {"batch_id": batch_id, "sensor_logs": logs, "count": len(logs)}


@router.get("/{batch_id}/recent")
async def get_recent_sensor_logs(
    batch_id: str,
    limit: int = 50,
    sensor_service: SensorService = Depends(get_sensor_service),
    current_user: dict = Depends(get_current_user),
):
    """Lấy sensor logs mới nhất của một batch (mặc định 50 records)."""
    logs = await sensor_service.get_recent_logs_by_batch_id(batch_id, limit=limit)
    return {"batch_id": batch_id, "sensor_logs": logs, "count": len(logs)}
