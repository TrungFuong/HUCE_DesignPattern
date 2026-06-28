from datetime import date, datetime
from enum import Enum, IntEnum


def to_plain_data(value):
    if isinstance(value, IntEnum):
        return int(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [to_plain_data(item) for item in value]
    if isinstance(value, dict):
        return {key: to_plain_data(item) for key, item in value.items()}
    if hasattr(value, "__dict__"):
        return to_plain_data(value.__dict__)
    return value
