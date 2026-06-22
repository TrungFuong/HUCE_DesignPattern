import json
from datetime import datetime

from app.domain.entities.sensor_log import SensorLog


class MqttMessageAdapter:

    def to_sensor_log(self, raw_message) -> SensorLog:
        payload = json.loads(raw_message.payload.decode())
        recorded_at = self._parse_recorded_at(payload.get("recorded_at"))
        return SensorLog(
            id=payload.get("id", ""),
            batch_id=payload["batch_id"],
            temperature=float(payload["temperature"]),
            humidity=float(payload["humidity"]),
            soil_moisture=payload.get("soil_moisture"),
            recorded_at=recorded_at,
        )

    @staticmethod
    def _parse_recorded_at(value) -> datetime:
        if not value:
            return datetime.utcnow()
        try:
            return datetime.fromisoformat(str(value))
        except (ValueError, TypeError):
            return datetime.utcnow()
