from enum import Enum


class RoleName(str, Enum):
    ADMIN = "ADMIN"
    FARMER = "FARMER"
    DISTRIBUTOR = "DISTRIBUTOR"
    IMPORTER = "IMPORTER"
