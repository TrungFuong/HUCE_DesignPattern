from app.application.builders.trace_response_builder import TraceResponseBuilder
from app.application.utils.serialization import to_plain_data


class TraceabilityFacade:

    def __init__(
        self,
        batch_service,
        farm_service,
        shipment_service,
        sensor_service,
        blockchain_service,
        hash_service,
        user_service=None,
        container_service=None,
        trace_response_builder: TraceResponseBuilder | None = None,
    ):
        self.batch_service = batch_service
        self.farm_service = farm_service
        self.shipment_service = shipment_service
        self.sensor_service = sensor_service
        self.blockchain_service = blockchain_service
        self.hash_service = hash_service
        self.user_service = user_service
        self.container_service = container_service
        self.trace_response_builder = trace_response_builder or TraceResponseBuilder()

    async def trace_batch(self, batch_id: str):
        batch = await self.batch_service.get_by_id(batch_id)
        farm = await self.farm_service.get_by_id(batch.farm_id)
        shipments = await self.shipment_service.get_by_batch_id(batch_id)
        sensor_logs = await self.sensor_service.get_logs_by_batch_id(batch_id)
        current_hash = self.hash_service.hash_data({
            "batch": to_plain_data(batch),
            "farm": to_plain_data(farm) if farm else None,
            "shipments": [to_plain_data(shipment) for shipment in shipments],
            "sensor_logs": [to_plain_data(log) for log in sensor_logs],
        })
        blockchain_hash = await self.blockchain_service.get_hash(batch_id)
        is_verified = current_hash == blockchain_hash
        return (
            self.trace_response_builder
            .with_batch(batch)
            .with_farm(farm)
            .with_shipment(shipments)
            .with_sensor_logs(sensor_logs)
            .with_verification(is_verified)
            .with_hashes(current_hash, blockchain_hash)
            .build()
        )

    async def trace_batch_public(self, batch_id: str):
        batch = await self.batch_service.get_by_id(batch_id)
        farm = await self.farm_service.get_by_id(batch.farm_id)
        shipments = await self.shipment_service.get_by_batch_id(batch_id)
        sensor_logs = await self.sensor_service.get_logs_by_batch_id(batch_id)
        current_hash = self.hash_service.hash_data({
            "batch": to_plain_data(batch),
            "farm": to_plain_data(farm) if farm else None,
            "shipments": [to_plain_data(shipment) for shipment in shipments],
            "sensor_logs": [to_plain_data(log) for log in sensor_logs],
        })
        blockchain_hash = await self.blockchain_service.get_hash(batch_id)
        return {
            "product": {
                "name": batch.product_name,
                "harvest_date": batch.harvest_date,
                "quantity": batch.quantity,
                "quantity_unit": batch.quantity_unit,
                "grade": batch.grade,
                "status": batch.status.name,
                "risk_level": batch.risk_level.name,
            },
            "farm": await self._build_public_farm(farm),
            "shipments": [await self._build_public_shipment(shipment) for shipment in shipments],
            "sensor_logs": [
                {
                    "temperature": log.temperature,
                    "humidity": log.humidity,
                    "soil_moisture": log.soil_moisture,
                    "recorded_at": log.recorded_at,
                }
                for log in sensor_logs
            ],
            "verification": {
                "is_verified": current_hash == blockchain_hash,
                "current_hash": current_hash,
                "blockchain_hash": blockchain_hash,
            },
        }

    async def _build_public_farm(self, farm):
        if farm is None:
            return None
        owner = await self._get_user(farm.owner_id)
        return {
            "name": farm.name,
            "address": farm.address,
            "planting_date": farm.planting_date,
            "harvest_date": farm.harvest_date,
            "owner": self._public_user(owner),
        }

    async def _build_public_shipment(self, shipment):
        shipment_data = shipment if isinstance(shipment, dict) else shipment.__dict__
        from_actor = await self._get_user(shipment_data["from_actor_id"])
        to_actor = await self._get_user(shipment_data["to_actor_id"])
        carrier = await self._get_user(shipment_data["carrier_id"])
        return {
            "from": self._public_user(from_actor),
            "to": self._public_user(to_actor),
            "carrier": self._public_user(carrier),
            "origin": shipment_data["origin"],
            "destination": shipment_data["destination"],
            "status": shipment_data["status"].name if hasattr(shipment_data["status"], "name") else shipment_data["status"],
            "start_time": shipment_data["start_time"],
            "end_time": shipment_data["end_time"],
            "notes": shipment_data["notes"],
            "items": [await self._build_public_shipment_item(item) for item in shipment_data.get("items", [])],
        }

    async def _build_public_shipment_item(self, item):
        item_data = item if isinstance(item, dict) else item.__dict__
        batch = await self.batch_service.get_by_id(item_data["batch_id"])
        container = await self._get_container(item_data["container_id"])
        return {
            "product_name": batch.product_name,
            "quantity": item_data["quantity"],
            "quantity_unit": item_data["quantity_unit"],
            "container": self._public_container(container),
        }

    async def _get_user(self, user_id: str):
        if self.user_service is None:
            return None
        return await self.user_service.get_by_id(user_id)

    async def _get_container(self, container_id: str):
        if self.container_service is None:
            return None
        try:
            return await self.container_service.get_by_id(container_id)
        except ValueError:
            return None

    def _public_user(self, user):
        if user is None:
            return None
        return {
            "full_name": user.full_name,
            "role": user.role.name,
        }

    def _public_container(self, container):
        if container is None:
            return None
        return {
            "code": container.code,
            "type": container.type,
            "capacity": container.capacity,
            "capacity_unit": container.capacity_unit,
            "material": container.material,
            "is_temperature_controlled": container.is_temperature_controlled,
            "min_temperature": container.min_temperature,
            "max_temperature": container.max_temperature,
            "status": container.status.name if hasattr(container.status, "name") else container.status,
            "description": container.description,
        }
