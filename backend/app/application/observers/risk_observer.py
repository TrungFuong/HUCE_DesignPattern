from app.application.observers.sensor_event_observer import SensorEventObserver
from app.domain.enums.risk_level import RiskLevel


class RiskObserver(SensorEventObserver):

    def __init__(self, risk_service, batch_service, farm_service=None):
        self.risk_service = risk_service
        self.batch_service = batch_service
        self.farm_service = farm_service

    async def update(self, sensor_log):
        crop_type = None
        if self.farm_service is not None:
            batch = await self.batch_service.get_by_id(sensor_log.batch_id)
            farm = await self.farm_service.get_by_id(batch.farm_id)
            crop_type = farm.crop_type

        risk_level = await self.risk_service.classify_sensor_log(sensor_log, crop_type=crop_type)
        if risk_level == RiskLevel.AT_RISK:
            await self.batch_service.mark_batch_at_risk(sensor_log.batch_id)
