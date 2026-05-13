from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlockchainRecord:
    id: str
    batch_id: str
    data_hash: str
    transaction_hash: str
    created_at: datetime
