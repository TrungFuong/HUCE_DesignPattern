from abc import ABC, abstractmethod


class RiskHandler(ABC):

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    async def handle(self, context):
        result = await self.check(context)
        if result is not None:
            return result
        if self.next_handler:
            return await self.next_handler.handle(context)
        return None

    @abstractmethod
    async def check(self, context):
        pass


class TemperatureRiskHandler(RiskHandler):

    async def check(self, context):
        sensor_log = context["sensor_log"]
        rule = context["rule"]
        if sensor_log.temperature > rule.max_temperature:
            return "TEMPERATURE_RISK"
        return None


class HumidityRiskHandler(RiskHandler):

    async def check(self, context):
        sensor_log = context["sensor_log"]
        rule = context["rule"]
        if sensor_log.humidity > rule.max_humidity:
            return "HUMIDITY_RISK"
        return None


class SoilRiskHandler(RiskHandler):

    async def check(self, context):
        sensor_log = context["sensor_log"]
        rule = context["rule"]
        if sensor_log.soil_moisture is None:
            return None
        if sensor_log.soil_moisture > (rule.max_soil_moisture or 0):
            return "SOIL_RISK"
        return None
