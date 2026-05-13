from dataclasses import dataclass


@dataclass
class Container:
    id: str
    code: str
    type: str
    description: str | None = None
