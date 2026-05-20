from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.batch_status import BatchStatus
from app.domain.enums.risk_level import RiskLevel


@dataclass
class Batch:
    id: str
    farm_id: str
    crop_type_id: str
    product_name: str
    harvest_date: datetime
    quantity: float
    quantity_unit: str
    grade: str | None
    status: BatchStatus
    risk_level: RiskLevel
    qr_code_url: str | None = None

    def mark_at_risk(self) -> None:
        self.risk_level = RiskLevel.AT_RISK

    def mark_normal(self) -> None:
        self.risk_level = RiskLevel.NORMAL
