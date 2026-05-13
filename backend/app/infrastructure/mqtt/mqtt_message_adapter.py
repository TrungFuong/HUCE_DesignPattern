import json
from datetime import datetime

from app.domain.entities.sensor_log import SensorLog


class MqttMessageAdapter:

    def to_sensor_log(self, raw_message) -> SensorLog:
        payload = json.loads(raw_message.payload.decode())
        return SensorLog(
            id=payload.get("id", ""),
            batch_id=payload["batch_id"],
            temperature=float(payload["temperature"]),
            humidity=float(payload["humidity"]),
            soil_moisture=payload.get("soil_moisture"),
            recorded_at=datetime.fromisoformat(payload["recorded_at"]),
        )
