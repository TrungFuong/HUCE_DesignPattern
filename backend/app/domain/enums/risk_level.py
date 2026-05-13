from enum import Enum


class RiskLevel(str, Enum):
    NORMAL = "NORMAL"
    AT_RISK = "AT_RISK"
