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
