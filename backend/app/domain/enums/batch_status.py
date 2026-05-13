from enum import Enum


class BatchStatus(str, Enum):
    CREATED = "CREATED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CLOSED = "CLOSED"
