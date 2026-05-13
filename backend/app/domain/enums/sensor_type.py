from enum import Enum


class SensorType(str, Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    SOIL_MOISTURE = "SOIL_MOISTURE"
