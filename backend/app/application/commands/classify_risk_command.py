from app.application.commands.command import Command
from app.application.services.risk_service import RiskService
from app.application.services.batch_service import BatchService
from app.domain.entities.sensor_log import SensorLog
from app.domain.enums.risk_level import RiskLevel


class ClassifyRiskCommand(Command):

    def __init__(self, sensor_log: SensorLog, risk_service: RiskService, batch_service: BatchService):
        self.sensor_log = sensor_log
        self.risk_service = risk_service
        self.batch_service = batch_service

    async def execute(self):
        risk_level = await self.risk_service.classify_sensor_log(self.sensor_log)
        if risk_level == RiskLevel.AT_RISK:
            await self.batch_service.mark_batch_at_risk(self.sensor_log.batch_id)
        return risk_level
