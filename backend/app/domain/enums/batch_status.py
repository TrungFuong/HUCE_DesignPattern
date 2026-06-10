from enum import IntEnum


class BatchStatus(IntEnum):
    CREATED = 0
    IN_TRANSIT = 1
    DELIVERED = 2
    CLOSED = 3
