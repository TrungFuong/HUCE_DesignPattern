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
        if shipment:
            self.payload["shipment"] = {
                "shipment_id": shipment.id,
                "container_id": shipment.container_id,
                "start_time": shipment.start_time.isoformat(),
                "end_time": shipment.end_time.isoformat() if shipment.end_time else None,
            }
        return self

    def build(self):
        return self.payload
