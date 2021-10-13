from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values_list(cls):
        return [key.value for key in cls]


class ResponseType(BaseEnum):
    VERIFY = "verify"
    ONBOARD = "onboard"
