from app.application.observers.sensor_event_observer import SensorEventObserver
from app.infrastructure.queue.queue_names import QueueName


class BlockchainObserver(SensorEventObserver):

    def __init__(self, queue_client):
        self.queue_client = queue_client

    async def update(self, sensor_log):
        await self.queue_client.push(QueueName.BLOCKCHAIN_HASH_QUEUE, {
            "batch_id": sensor_log.batch_id,
            "sensor_log_id": sensor_log.id,
        })
