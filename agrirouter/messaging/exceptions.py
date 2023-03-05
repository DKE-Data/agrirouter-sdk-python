from agrirouter.onboarding.exceptions import AgrirouterBaseException


class TypeUrlNotFoundError(AgrirouterBaseException):
    _message = "Given type url not found"


class WrongFieldError(AgrirouterBaseException):
    _message = "Unknown field"


class DecodeMessageException(AgrirouterBaseException):
    _message = "Can't decode message"


class OutboxException(AgrirouterBaseException):
    _message = "Can't fetch outbox message"
