class AgrirouterBaseException(Exception):
    """ Base class for Agrirouter exceptions. """
    _message = ...

    def __init__(self, message=None):
        """ Initialize the exception and define the message. """
        if not message:
            message = self._message
        self.message = message


class WrongCertificationType(AgrirouterBaseException):
    """ Exception for wrong certification type. """
    _message = "Wrong Certification type. Use 'onboarding.enums.CertificationTypes' values instead."


class WrongGateWayType(AgrirouterBaseException):
    """ Exception if there is wrong gateway Type. """
    _message = "Wrong Gate Way Id. Use onboarding.enums.GateWays values instead."


class RequestNotSigned(AgrirouterBaseException):
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
