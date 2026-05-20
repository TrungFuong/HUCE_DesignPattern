class BatchHashPayloadBuilder:

    def __init__(self):
        self.payload = {}

    def with_batch(self, batch):
        self.payload["batch_id"] = batch.id
        self.payload["product_name"] = batch.product_name
        self.payload["farm_id"] = batch.farm_id
        self.payload["harvest_date"] = batch.harvest_date.isoformat()
        return self

    def with_sensor_logs(self, sensor_logs):
        self.payload["sensor_logs"] = [
            {
                "temperature": log.temperature,
                "humidity": log.humidity,
                "soil_moisture": log.soil_moisture,
                "recorded_at": log.recorded_at.isoformat(),
            }
            for log in sensor_logs
        ]
        return self

    def with_shipment(self, shipment):
        shipments = shipment if isinstance(shipment, list) else ([shipment] if shipment else [])
        self.payload["shipments"] = shipments
        return self

    def build(self):
        return self.payload
