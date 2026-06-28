import asyncio

from app.application.commands.write_hash_to_blockchain_command import WriteHashToBlockchainCommand
from app.application.services.batch_service import BatchService
from app.application.services.blockchain_service import BlockchainService
from app.application.services.farm_service import FarmService
from app.application.services.sensor_service import SensorService
from app.application.services.shipment_service import ShipmentService
from app.infrastructure.blockchain.blockchain_proxy import BlockchainProxy
from app.infrastructure.blockchain.smart_contract_adapter import SmartContractAdapter
from app.infrastructure.blockchain.web3_client import Web3Client
from app.infrastructure.database.mongodb.mongo_client import get_mongo_database
from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.queue.redis_client import get_redis_client
from app.infrastructure.queue.redis_queue_adapter import RedisQueueAdapter
from app.infrastructure.queue.queue_names import QueueName
from app.infrastructure.qr.qr_code_service import QrCodeService
from app.infrastructure.hashing.sha256_hash_service import Sha256HashService
from app.core.config import settings


class BlockchainWorker:

    def __init__(self, queue_client=None):
        self.queue_client = queue_client or RedisQueueAdapter(get_redis_client())

    async def start(self) -> None:
        while True:
            job = await self.queue_client.pop(QueueName.BLOCKCHAIN_HASH_QUEUE)
            if job is None:
                await asyncio.sleep(1)
                continue
            try:
                batch_id = job.get("batch_id")
                if not batch_id:
                    raise ValueError("Blockchain job missing batch_id")
                reason = job.get("reason", "UNKNOWN")
                print(f"[BlockchainWorker] Processing job batch_id={batch_id} reason={reason}")
                await self._process_job(batch_id)
                print(f"[BlockchainWorker] Hash written to blockchain for batch_id={batch_id}")
            except Exception as error:
                print(f"[BlockchainWorker] Error processing job: {error}")
                await asyncio.sleep(1)

    async def _process_job(self, batch_id: str) -> None:
        web3 = Web3Client(settings.blockchain_rpc_url)
        contract = web3.get_contract(settings.contract_address)
        blockchain_client = SmartContractAdapter(web3=web3, contract=contract)
        blockchain_proxy = BlockchainProxy(blockchain_client=blockchain_client, cache_client=get_redis_client())
        blockchain_service = BlockchainService(blockchain_client=blockchain_proxy)
        hash_service = Sha256HashService()

        async with get_async_session() as session:
            batch_service = BatchService(
                batch_repository=SqlBatchRepository(session),
                qr_service=QrCodeService(),
            )
            farm_service = FarmService(SqlFarmRepository(session), SqlUserRepository(session))
            shipment_service = ShipmentService(
                shipment_repository=SqlShipmentRepository(session),
                batch_repository=SqlBatchRepository(session),
                user_repository=SqlUserRepository(session),
                container_repository=SqlContainerRepository(session),
            )
            sensor_service = SensorService(MongoSensorLogRepository(get_mongo_database()))

            command = WriteHashToBlockchainCommand(
                batch_id=batch_id,
                batch_service=batch_service,
                farm_service=farm_service,
                shipment_service=shipment_service,
                sensor_service=sensor_service,
                blockchain_service=blockchain_service,
                hash_service=hash_service,
            )
            await command.execute()

