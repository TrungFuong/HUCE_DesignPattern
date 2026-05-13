class TraceResponseBuilder:

    def __init__(self):
        self.response = {}

    def with_batch(self, batch):
        self.response["batch"] = batch.__dict__ if hasattr(batch, "__dict__") else batch
        return self

    def with_farm(self, farm):
        self.response["farm"] = farm.__dict__ if farm else None
        return self

    def with_shipment(self, shipment):
        self.response["shipment"] = shipment.__dict__ if shipment else None
        return self

    def with_sensor_logs(self, sensor_logs):
        self.response["sensor_logs"] = [log.__dict__ for log in sensor_logs]
        return self

    def with_verification(self, is_verified: bool):
        self.response["is_verified"] = is_verified
        return self

    def build(self):
        return self.response
