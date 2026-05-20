from app.application.observers.sensor_event_observer import SensorEventObserver
from app.domain.enums.risk_level import RiskLevel


class RiskObserver(SensorEventObserver):

    def __init__(self, risk_service, batch_service):
        self.risk_service = risk_service
        self.batch_service = batch_service

    async def update(self, sensor_log):
        batch = await self.batch_service.get_by_id(sensor_log.batch_id)
        crop_type_id = getattr(batch, "crop_type_id", None)

        risk_level = await self.risk_service.classify_sensor_log(sensor_log, crop_type_id=crop_type_id)
        if risk_level == RiskLevel.AT_RISK:
            await self.batch_service.mark_batch_at_risk(sensor_log.batch_id)
