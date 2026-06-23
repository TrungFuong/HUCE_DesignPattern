# app/workers/command_worker.py
# Pattern: Command — dùng CommandDispatcher để thực thi các Command object
import asyncio

from app.application.commands.classify_risk_command import ClassifyRiskCommand
from app.application.commands.command_dispatcher import CommandDispatcher
from app.application.commands.save_sensor_log_command import SaveSensorLogCommand
from app.application.services.batch_service import BatchService
from app.application.services.risk_service import RiskService
from app.application.services.sensor_service import SensorService
from app.domain.entities.sensor_log import SensorLog
from app.infrastructure.database.mongodb.mongo_client import get_mongo_database
from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_risk_rule_repository import SqlRiskRuleRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.queue.queue_names import QueueName
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.infrastructure.qr.qr_code_service import QrCodeService
from datetime import datetime


class CommandWorker:
    """
    Worker sử dụng Command Pattern + CommandDispatcher.
    Mỗi message từ queue được đóng gói thành Command object rồi dispatch để thực thi.
    Đây là alternative pipeline so với SensorWorker (trực tiếp gọi service).
    """

    def __init__(self, queue_client=None):
        self.queue_client = queue_client or RedisQueueAdapter(get_redis_client())
        self.dispatcher = CommandDispatcher()
        self.mongo_db = get_mongo_database()

    async def start(self) -> None:
        print("[CommandWorker] Starting... (polling command_sensor_queue via CommandDispatcher)")
        while True:
            message = await self.queue_client.pop(QueueName.SENSOR_LOG_QUEUE)
            if message is None:
                await asyncio.sleep(1)
                continue
            try:
                sensor_log = self._build_sensor_log(message)
                print(f"[CommandWorker] Dispatching commands for batch_id={sensor_log.batch_id}")
                await self._dispatch_commands(sensor_log)
            except Exception as error:
                print(f"[CommandWorker] Error: {error}")
                await asyncio.sleep(1)

    async def _dispatch_commands(self, sensor_log: SensorLog) -> None:
        """Tạo Command objects và dispatch qua CommandDispatcher."""
        # Command 1: SaveSensorLogCommand
        sensor_service = SensorService(MongoSensorLogRepository(self.mongo_db))
        save_cmd = SaveSensorLogCommand(sensor_log=sensor_log, sensor_service=sensor_service)
        await self.dispatcher.dispatch(save_cmd)
        print(f"[CommandWorker] SaveSensorLogCommand executed for batch_id={sensor_log.batch_id}")

        # Command 2: ClassifyRiskCommand
        async with get_async_session() as session:
            risk_service = RiskService(SqlRiskRuleRepository(session))
            batch_service = BatchService(
                batch_repository=SqlBatchRepository(session),
                qr_service=QrCodeService(),
            )
            risk_cmd = ClassifyRiskCommand(
                sensor_log=sensor_log,
                risk_service=risk_service,
                batch_service=batch_service,
            )
            risk_level = await self.dispatcher.dispatch(risk_cmd)
            print(f"[CommandWorker] ClassifyRiskCommand executed — risk={risk_level} batch_id={sensor_log.batch_id}")

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
