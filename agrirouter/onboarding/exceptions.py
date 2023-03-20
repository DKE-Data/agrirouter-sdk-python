class AgrirouterBaseException(Exception):
    _message = ...

    def __init__(self, message=None):
        if not message:
            message = self._message
        self.message = message


class WrongCertificationType(AgrirouterBaseException):
    _message = "Wrong Certification type. Use onboarding.enums.CertificationTypes values instead."


class WrongGateWay(AgrirouterBaseException):
    _message = "Wrong Gate Way Id. Use onboarding.enums.GateWays values instead."


class RequestNotSigned(AgrirouterBaseException):
    _message = """
    Request does not contain signature header. Please sign the request with request.sign() method.\n
    Details on: https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/
    integration/onboarding.html#signing-requests
    """


class BadMessagingResult(AgrirouterBaseException):
    _message = "Messaging Request failed"

class OnboardException(AgrirouterBaseException):
    _message = "Unexpected error during onboarding."

