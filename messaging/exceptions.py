from onboarding.exceptions import AgriRouuterBaseException


class TypeUrlNotFoundError(AgriRouuterBaseException):
    _message = "Given type url not found"
