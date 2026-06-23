import asyncio
from datetime import datetime
from typing import Any

from app.application.services.batch_service import BatchService
from app.application.services.risk_service import RiskService
from app.application.services.sensor_service import SensorService
from app.domain.entities.sensor_log import SensorLog
from app.domain.enums.risk_level import RiskLevel
from app.infrastructure.database.mongodb.mongo_client import get_mongo_database
from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.infrastructure.queue.queue_names import QueueName
from app.infrastructure.qr.qr_code_service import QrCodeService


class SensorWorker:

    def __init__(self, queue_client=None):
        self.queue_client = queue_client or RedisQueueAdapter(get_redis_client())
        self.mongo_db = get_mongo_database()

    async def start(self) -> None:
        while True:
            message = await self.queue_client.pop(QueueName.SENSOR_LOG_QUEUE)
            if message is None:
                await asyncio.sleep(1)
                continue
            try:
                sensor_log = self._build_sensor_log(message)
                print(f"[SensorWorker] Processing sensor log batch_id={sensor_log.batch_id}")
                await self._process_sensor_log(sensor_log)
            except Exception as error:
                print(f"[SensorWorker] Error processing message: {error}")
                await asyncio.sleep(1)

    def _build_sensor_log(self, data: dict[str, Any]) -> SensorLog:
        recorded_at = data.get("recorded_at")
        if isinstance(recorded_at, str):
            recorded_at = datetime.fromisoformat(recorded_at)
        return SensorLog(
            id=str(data.get("id") or ""),
            batch_id=str(data["batch_id"]),
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            soil_moisture=None if data.get("soil_moisture") is None else float(data["soil_moisture"]),
            recorded_at=recorded_at,
        )

    async def _process_sensor_log(self, sensor_log: SensorLog) -> None:
        sensor_service = SensorService(MongoSensorLogRepository(self.mongo_db))
        await sensor_service.save_sensor_log(sensor_log)
        print(f"[SensorWorker] Saved sensor log to MongoDB batch_id={sensor_log.batch_id}")

        async with get_async_session() as session:
            batch_service = BatchService(
                batch_repository=SqlBatchRepository(session),
                qr_service=QrCodeService(),
            )
            risk_service = RiskService(SqlRiskRuleRepository(session))
            batch = await batch_service.get_by_id(sensor_log.batch_id)
            crop_type_id = getattr(batch, "crop_type_id", None)
            risk_level = await risk_service.classify_sensor_log(sensor_log, crop_type_id=crop_type_id)
            print(f"[SensorWorker] Risk classified: {risk_level.name} for batch_id={sensor_log.batch_id}")
            if risk_level == RiskLevel.AT_RISK:
                await batch_service.mark_batch_at_risk(sensor_log.batch_id)
                print(f"[SensorWorker] Batch marked AT_RISK: batch_id={sensor_log.batch_id}")

        await self.queue_client.push(
            QueueName.BLOCKCHAIN_HASH_QUEUE,
            {
                "batch_id": sensor_log.batch_id,
                "reason": "SENSOR_LOG_SAVED",
            },
        )
