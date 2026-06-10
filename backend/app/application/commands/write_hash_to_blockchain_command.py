from app.application.commands.command import Command
from app.application.utils.serialization import to_plain_data
from app.application.services.batch_service import BatchService
from app.application.services.sensor_service import SensorService
from app.application.services.blockchain_service import BlockchainService
from app.infrastructure.hashing.sha256_hash_service import Sha256HashService


class WriteHashToBlockchainCommand(Command):

    def __init__(self, batch_id: str, batch_service: BatchService, sensor_service: SensorService, blockchain_service: BlockchainService, hash_service: Sha256HashService):
        self.batch_id = batch_id
        self.batch_service = batch_service
        self.sensor_service = sensor_service
        self.blockchain_service = blockchain_service
        self.hash_service = hash_service

    async def execute(self):
        batch = await self.batch_service.get_by_id(self.batch_id)
        sensor_logs = await self.sensor_service.get_logs_by_batch_id(self.batch_id)
        payload = {
            "batch": to_plain_data(batch),
            "sensor_logs": [to_plain_data(log) for log in sensor_logs],
        }
        data_hash = self.hash_service.hash_data(payload)
        return await self.blockchain_service.write_hash(batch_id=self.batch_id, data_hash=data_hash)
