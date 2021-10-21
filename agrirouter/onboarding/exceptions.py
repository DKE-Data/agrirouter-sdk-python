class AgriRouuterBaseException(Exception):
    _message = ...

    def __init__(self, message=None):
        if not message:
            message = self._message
        self.message = message


class WrongCertificationType(AgriRouuterBaseException):
    _message = "Wrong Certification type. Use onboarding.enums.CertificationTypes values instead."


class WrongGateWay(AgriRouuterBaseException):
    _message = "Wrong Gate Way Id. Use onboarding.enums.GateWays values instead."


class RequestNotSigned(AgriRouuterBaseException):
    _message = """
    Request does not contain signature header. Please sign the request with request.sign() method.\n
    Details on: https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/
    integration/onboarding.html#signing-requests
    """


class BadMessagingResult(AgriRouuterBaseException):
    _message = "Messaging Request failed"
