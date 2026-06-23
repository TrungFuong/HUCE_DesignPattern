from app.domain.entities.sensor_log import SensorLog
from app.domain.interfaces.repositories.sensor_log_repository import SensorLogRepository


class SensorService:

    def __init__(self, sensor_log_repository: SensorLogRepository):
        self.sensor_log_repository = sensor_log_repository

    async def save_sensor_log(self, sensor_log):
        if not isinstance(sensor_log, SensorLog):
            data = sensor_log.model_dump() if hasattr(sensor_log, "model_dump") else sensor_log.__dict__
            sensor_log = SensorLog(**data)
        return await self.sensor_log_repository.save(sensor_log)

    async def get_logs_by_batch_id(self, batch_id: str):
        return await self.sensor_log_repository.find_by_batch_id(batch_id)

    async def get_recent_logs_by_batch_id(self, batch_id: str, limit: int = 50):
        return await self.sensor_log_repository.find_recent_by_batch_id(batch_id, limit=limit)
