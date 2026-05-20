from dataclasses import dataclass


@dataclass
class CropType:
    id: str
    code: str
    name: str
    description: str | None = None
