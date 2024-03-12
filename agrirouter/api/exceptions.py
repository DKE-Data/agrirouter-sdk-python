class AgrirouterBaseException(Exception):
    """ Base class for internal exceptions. """
    _message = ...

    def __init__(self, message=None):
        """ Initialize the exception and define the message. """
        if not message:
            message = self._message
        self.message = message


class BadAuthResponse(AgrirouterBaseException):
    _message = "Bad Response. Response could is not verified."


class InvalidEnvironmentSetup(AgrirouterBaseException):
    _message = "Invalid value of env parameter. [QA] or [Production] values are allowed. " \
               "Please use environments.enums.Environments enum for configure environment properly"


class TypeUrlNotFoundError(AgrirouterBaseException):
    _message = "Given type url not found"


class WrongFieldError(AgrirouterBaseException):
    _message = "Unknown field"


class DecodeMessageException(AgrirouterBaseException):
    _message = "Can't decode message"


class OutboxException(AgrirouterBaseException):
    _message = "Can't fetch outbox message"


class WrongCertificationType(AgrirouterBaseException):
    """ Exception for wrong certification type. """
    _message = "Wrong Certification type. Use 'onboarding.enums.CertificationTypes' values instead."


class WrongGateWayType(AgrirouterBaseException):
    """ Exception if there is wrong gateway Type. """
    _message = "Wrong Gate Way Id. Use onboarding.enums.GateWays values instead."


class RequestNotSignedException(AgrirouterBaseException):
    """ Exception if request is not signed correctly. """
    _message = """
    Request does not contain signature header. Please sign the request with request.sign() method.\n
    Details on: https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/
    integration/onboarding.html#signing-requests
    """


class BadMessagingResult(AgrirouterBaseException):
    """ Exception if the messaging result is not ok. """
    _message = "Messaging request failed"


class OnboardException(AgrirouterBaseException):
    """ Exception if onboarding failed (most likely in case of an unexpected error). """
    _message = "Unexpected error during onboarding."
