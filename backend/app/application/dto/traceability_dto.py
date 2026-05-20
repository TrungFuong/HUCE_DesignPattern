from typing import Any
from pydantic import BaseModel


class TraceabilityResponse(BaseModel):
    batch: dict[str, Any]
    farm: dict[str, Any] | None
    shipment: dict[str, Any] | None
    shipments: list[dict[str, Any]]
    sensor_logs: list[dict[str, Any]]
    is_verified: bool
    current_hash: str | None = None
    blockchain_hash: str | None = None
