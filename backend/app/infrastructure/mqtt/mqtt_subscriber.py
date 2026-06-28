from app.infrastructure.mqtt.hive_mqtt_client import HiveMqttClient
from app.infrastructure.mqtt.mqtt_message_adapter import MqttMessageAdapter
from app.infrastructure.queue.queue_names import QueueName
from app.domain.entities.sensor_log import SensorLog
from app.domain.interfaces.services.queue_client import QueueClient


class MqttSubscriber:

    def __init__(
        self,
        mqtt_client: HiveMqttClient,
        message_adapter: MqttMessageAdapter,
        queue_client: QueueClient,
        topic: str,
    ):
        self.mqtt_client = mqtt_client
        self.message_adapter = message_adapter
        self.queue_client = queue_client
        self.topic = topic

    async def on_message(self, raw_message) -> None:
        try:
            sensor_log = self.message_adapter.to_sensor_log(raw_message)
            payload = self._serialize_sensor_log(sensor_log)
            print(f"[MQTT] Received sensor log for batch_id={sensor_log.batch_id} temp={sensor_log.temperature}")
            await self.queue_client.push(QueueName.SENSOR_LOG_QUEUE, payload)
            print(f"[MQTT] Pushed to sensor_log_queue: batch_id={sensor_log.batch_id}")
        except Exception as error:
            print(f"[MQTT] Error processing message: {error}")

    def _serialize_sensor_log(self, sensor_log: SensorLog) -> dict:
        data = sensor_log.__dict__.copy()
        recorded_at = data.get("recorded_at")
        if hasattr(recorded_at, "isoformat"):
            data["recorded_at"] = recorded_at.isoformat()
        return data

    async def start(self) -> None:
        await self.mqtt_client.connect_and_subscribe(self.topic, self.on_message)
