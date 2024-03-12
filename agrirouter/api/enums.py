from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values_list(cls):
        return [key.value for key in cls]


class ResponseTypes(BaseEnum):
    VERIFY = "verify"
    ONBOARD = "onboard"


class ContentTypes(BaseEnum):
    APPLICATION_JSON = "application/json"


class Environments(BaseEnum):
    PRODUCTION: str = "production"
    QA: str = "qa"


class RequestHeaders(BaseEnum):
    AUTHORIZATION: str = "Authorization"
    X_AGRIROUTER_SIGNATURE: str = "X-Agrirouter-Signature"
    CONTENT_TYPE: str = "Content-Type"
    X_AGRIROUTER_APPLICATION_ID: str = "X-Agrirouter-ApplicationId"
