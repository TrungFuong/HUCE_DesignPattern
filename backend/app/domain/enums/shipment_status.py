from enum import IntEnum


class ShipmentStatus(IntEnum):
    CREATED = 0
    IN_TRANSIT = 1
    DELIVERED = 2
    CANCELLED = 3
