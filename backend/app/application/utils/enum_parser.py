from enum import Enum


def parse_enum(enum_class: type[Enum], value):
    if isinstance(value, enum_class):
        return value
    if isinstance(value, str):
        normalized = value.strip()
        if normalized.isdigit():
            return enum_class(int(normalized))
        return enum_class[normalized.upper()]
    return enum_class(value)


def format_enum_options(enum_class: type[Enum]) -> str:
    return ", ".join([f"{item.name}:{item.value}" for item in enum_class])
