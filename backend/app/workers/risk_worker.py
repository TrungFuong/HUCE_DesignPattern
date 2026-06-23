# app/workers/risk_worker.py
# RiskWorker: xử lý riêng risk classification jobs từ Redis queue
import asyncio
from datetime import datetime

from app.application.services.batch_service import BatchService
from app.application.services.risk_service import RiskService
from app.domain.entities.sensor_log import SensorLog
from app.domain.enums.risk_level import RiskLevel
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.queue.queue_names import QueueName
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.infrastructure.qr.qr_code_service import QrCodeService


RISK_JOB_QUEUE = "risk_classify_queue"


class RiskWorker:
    """
    Worker chuyên xử lý risk classification jobs.
    Nhận sensor_log data từ Redis queue, classify risk và cập nhật batch status.
    Có thể dùng song song với SensorWorker hoặc thay thế phần risk của nó.
    """

    def __init__(self, queue_client=None):
        self.queue_client = queue_client or RedisQueueAdapter(get_redis_client())

    async def start(self) -> None:
        print(f"[RiskWorker] Starting... (polling {RISK_JOB_QUEUE})")
        while True:
            message = await self.queue_client.pop(RISK_JOB_QUEUE)
            if message is None:
                await asyncio.sleep(1)
                continue
            try:
                sensor_log = self._build_sensor_log(message)
                print(f"[RiskWorker] Classifying risk for batch_id={sensor_log.batch_id}")
                await self._classify_and_update(sensor_log)
            except Exception as error:
                print(f"[RiskWorker] Error: {error}")
                await asyncio.sleep(1)

    async def _classify_and_update(self, sensor_log: SensorLog) -> None:
        async with get_async_session() as session:
            risk_service = RiskService(SqlRiskRuleRepository(session))
            batch_service = BatchService(
                batch_repository=SqlBatchRepository(session),
                qr_service=QrCodeService(),
            )
            batch = await batch_service.get_by_id(sensor_log.batch_id)
            crop_type_id = getattr(batch, "crop_type_id", None)
            risk_level = await risk_service.classify_sensor_log(sensor_log, crop_type_id=crop_type_id)
            print(f"[RiskWorker] Risk={risk_level.name} batch_id={sensor_log.batch_id}")
            if risk_level == RiskLevel.AT_RISK:
                await batch_service.mark_batch_at_risk(sensor_log.batch_id)
                print(f"[RiskWorker] Batch marked AT_RISK: batch_id={sensor_log.batch_id}")

    @staticmethod
    def _build_sensor_log(data: dict) -> SensorLog:
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
