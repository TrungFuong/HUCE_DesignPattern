import logging

from app.application.observers.sensor_event_observer import SensorEventObserver

logger = logging.getLogger(__name__)


class DashboardObserver(SensorEventObserver):
    """
    Observer pattern: lắng nghe SensorEvent và log ra thông tin dashboard.
    Trong hệ thống thực, có thể broadcast qua WebSocket hoặc push notification.
    """

    async def update(self, sensor_log) -> None:
        logger.info(
            "[Dashboard] New sensor log received — batch_id=%s temp=%.1f humidity=%.1f soil=%s",
            sensor_log.batch_id,
            sensor_log.temperature,
            sensor_log.humidity,
            sensor_log.soil_moisture,
        )
        print(
            f"[Dashboard] batch_id={sensor_log.batch_id} "
            f"temp={sensor_log.temperature}°C "
            f"humidity={sensor_log.humidity}% "
            f"soil={sensor_log.soil_moisture}"
        )
