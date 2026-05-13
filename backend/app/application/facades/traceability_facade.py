from app.application.builders.trace_response_builder import TraceResponseBuilder


class TraceabilityFacade:

    def __init__(
        self,
        batch_service,
        farm_service,
        shipment_service,
        sensor_service,
        blockchain_service,
        hash_service,
        trace_response_builder: TraceResponseBuilder | None = None,
    ):
        self.batch_service = batch_service
        self.farm_service = farm_service
        self.shipment_service = shipment_service
        self.sensor_service = sensor_service
        self.blockchain_service = blockchain_service
        self.hash_service = hash_service
        self.trace_response_builder = trace_response_builder or TraceResponseBuilder()

    async def trace_batch(self, batch_id: str):
        batch = await self.batch_service.get_by_id(batch_id)
        farm = await self.farm_service.get_by_id(batch.farm_id)
        shipment = await self.shipment_service.get_by_batch_id(batch_id)
        sensor_logs = await self.sensor_service.get_logs_by_batch_id(batch_id)
        current_hash = self.hash_service.hash_data({
            "batch": batch.__dict__,
            "farm": farm.__dict__ if farm else None,
            "shipment": shipment.__dict__ if shipment else None,
            "sensor_logs": [log.__dict__ for log in sensor_logs],
        })
        blockchain_hash = await self.blockchain_service.get_hash(batch_id)
        is_verified = current_hash == blockchain_hash
        return (
            self.trace_response_builder
            .with_batch(batch)
            .with_farm(farm)
            .with_shipment(shipment)
            .with_sensor_logs(sensor_logs)
            .with_verification(is_verified)
            .build()
        )
