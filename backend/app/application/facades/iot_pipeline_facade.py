from app.application.observers.sensor_event import SensorEvent


class IoTPipelineFacade:

    def __init__(self, mongo_observer, risk_observer, blockchain_observer, dashboard_observer):
        self.mongo_observer = mongo_observer
        self.risk_observer = risk_observer
        self.blockchain_observer = blockchain_observer
        self.dashboard_observer = dashboard_observer

    async def process_sensor_log(self, sensor_log):
        event = SensorEvent(sensor_log)
        event.attach(self.mongo_observer)
        event.attach(self.risk_observer)
        event.attach(self.blockchain_observer)
        event.attach(self.dashboard_observer)
        await event.notify()
