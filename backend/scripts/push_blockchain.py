import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

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
from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository
from app.infrastructure.database.sqlserver.repositories.sql_container_repository import SqlContainerRepository
from app.infrastructure.database.sqlserver.repositories.sql_farm_repository import SqlFarmRepository
from app.infrastructure.database.sqlserver.repositories.sql_shipment_repository import SqlShipmentRepository
from app.infrastructure.database.sqlserver.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.database.sqlserver.session import get_async_session
from app.infrastructure.qr.qr_code_service import QrCodeService
from app.infrastructure.hashing.sha256_hash_service import Sha256HashService
from app.core.config import settings

class DummyCacheClient:
    async def get(self, key): return None
    async def set(self, key, val, ex=None): pass

async def main(batch_id: str):
    print(f"Pushing hash to blockchain for batch: {batch_id}")
    web3 = Web3Client(settings.blockchain_rpc_url)
    contract = web3.get_contract(settings.contract_address)
    blockchain_client = SmartContractAdapter(web3=web3, contract=contract)
    
    # Use dummy cache to avoid Redis dependency
    blockchain_proxy = BlockchainProxy(blockchain_client=blockchain_client, cache_client=DummyCacheClient())
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
        # For sensor logs, we need MongoDB running. If it fails, it will throw an error.
        sensor_service = SensorService(None) # Pass None to avoid mongo dependency if not strictly needed
        
        # Actually we need MongoSensorLogRepository for sensor logs
        try:
            from app.infrastructure.database.mongodb.repositories.mongo_sensor_log_repository import MongoSensorLogRepository
            sensor_service = SensorService(MongoSensorLogRepository(get_mongo_database()))
        except Exception as e:
            print("Mongo not available, using empty logs")
            
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
        print("Successfully written hash to blockchain!")

if __name__ == "__main__":
    batch_id = sys.argv[1] if len(sys.argv) > 1 else "2149604e-5948-4bd8-8f99-64622f7e7a98"
    asyncio.run(main(batch_id))
