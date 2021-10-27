from agrirouter.onboarding.exceptions import AgriRouuterBaseException


class TypeUrlNotFoundError(AgriRouuterBaseException):
    _message = "Given type url not found"


class WrongFieldError(AgriRouuterBaseException):
    _message = "Unknown field"


class DecodeMessageException(AgriRouuterBaseException):
    _message = "Can't decode message"


class OutboxException(AgriRouuterBaseException):
    _message = "Can't fetch outbox message"
