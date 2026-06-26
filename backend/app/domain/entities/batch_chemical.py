from dataclasses import dataclass
from datetime import datetime


@dataclass
class BatchChemical:
    batch_id: str
    chemical_id: str
    applied_at: datetime | None = None
