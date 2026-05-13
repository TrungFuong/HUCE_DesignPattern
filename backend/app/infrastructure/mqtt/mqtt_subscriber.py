from app.infrastructure.mqtt.hive_mqtt_client import HiveMqttClient
from app.infrastructure.mqtt.mqtt_message_adapter import MqttMessageAdapter
from app.application.facades.iot_pipeline_facade import IoTPipelineFacade


class MqttSubscriber:

    def __init__(self, mqtt_client: HiveMqttClient, message_adapter: MqttMessageAdapter, iot_pipeline_facade: IoTPipelineFacade):
        self.mqtt_client = mqtt_client
        self.message_adapter = message_adapter
        self.iot_pipeline_facade = iot_pipeline_facade

    async def on_message(self, raw_message):
        sensor_log = self.message_adapter.to_sensor_log(raw_message)
        await self.iot_pipeline_facade.process_sensor_log(sensor_log)

    async def start(self) -> None:
        await self.mqtt_client.connect()
        await self.mqtt_client.subscribe("ocop/sensors/#", self.on_message)
