from app.application.observers.sensor_event_observer import SensorEventObserver


class MongoSensorObserver(SensorEventObserver):

    def __init__(self, sensor_log_repository):
        self.sensor_log_repository = sensor_log_repository

    async def update(self, sensor_log):
        await self.sensor_log_repository.save(sensor_log)
