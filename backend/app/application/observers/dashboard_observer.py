from app.application.observers.sensor_event_observer import SensorEventObserver


class DashboardObserver(SensorEventObserver):

    async def update(self, sensor_log):
        # Placeholder: notify dashboard systems or analytics pipeline
        return True
