from app.application.commands.command import Command
from app.application.services.sensor_service import SensorService
from app.domain.entities.sensor_log import SensorLog


class SaveSensorLogCommand(Command):

    def __init__(self, sensor_log: SensorLog, sensor_service: SensorService):
        self.sensor_log = sensor_log
        self.sensor_service = sensor_service

    async def execute(self):
        return await self.sensor_service.save_sensor_log(self.sensor_log)
