import asyncio
import sys

from app.workers.blockchain_worker import BlockchainWorker
from app.workers.sensor_worker import SensorWorker


async def main(mode: str) -> None:
    tasks = []
    if mode in ("sensor", "all"):
        print("[Worker] SensorWorker starting... (polling sensor_log_queue)")
        tasks.append(SensorWorker().start())
    if mode in ("blockchain", "all"):
        print("[Worker] BlockchainWorker starting... (polling blockchain_hash_queue)")
        tasks.append(BlockchainWorker().start())

    if not tasks:
        print("Usage: python -m app.workers.worker_main [sensor|blockchain|all]")
        return

    print("[Worker] All workers running. Waiting for messages from Redis...")
    print("[Worker] Press Ctrl+C to stop.")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if mode not in ("sensor", "blockchain", "all"):
        print("Usage: python -m app.workers.worker_main [sensor|blockchain|all]")
        sys.exit(1)
    asyncio.run(main(mode))
