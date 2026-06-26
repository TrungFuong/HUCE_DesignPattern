from dataclasses import dataclass


@dataclass
class Chemical:
    id: str
    crop_type_id: str
    name: str
    unit: str
    description: str | None = None
    is_deleted: bool = False
