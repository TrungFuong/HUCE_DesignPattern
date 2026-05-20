from enum import IntEnum


class ContainerStatus(IntEnum):
    ACTIVE = 0
    IN_USE = 1
    MAINTENANCE = 2
    RETIRED = 3
