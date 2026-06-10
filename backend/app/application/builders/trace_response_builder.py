from app.application.utils.serialization import to_plain_data


class TraceResponseBuilder:

    def __init__(self):
        self.response = {}

    def with_batch(self, batch):
        self.response["batch"] = to_plain_data(batch)
        return self

    def with_farm(self, farm):
        self.response["farm"] = to_plain_data(farm) if farm else None
        return self

    def with_shipment(self, shipment):
        if isinstance(shipment, list):
            self.response["shipments"] = [to_plain_data(item) for item in shipment]
            self.response["shipment"] = self.response["shipments"][0] if shipment else None
        else:
            self.response["shipment"] = to_plain_data(shipment) if shipment else None
            self.response["shipments"] = [self.response["shipment"]] if shipment else []
        return self

    def with_sensor_logs(self, sensor_logs):
        self.response["sensor_logs"] = [to_plain_data(log) for log in sensor_logs]
        return self

    def with_verification(self, is_verified: bool):
        self.response["is_verified"] = is_verified
        return self

    def with_hashes(self, current_hash: str, blockchain_hash: str | None):
        self.response["current_hash"] = current_hash
        self.response["blockchain_hash"] = blockchain_hash
        return self

    def build(self):
        return self.response
