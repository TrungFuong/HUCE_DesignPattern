class SensorEvent:

    def __init__(self, sensor_log):
        self.sensor_log = sensor_log
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    async def notify(self):
        for observer in self.observers:
            await observer.update(self.sensor_log)
