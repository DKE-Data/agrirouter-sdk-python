from abc import ABC, abstractmethod

from agrirouter.constants.media_types import ContentTypes


class BaseOnboardingHeader(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        self._set_params(*args, **kwargs)

    @abstractmethod
    def get_header(self) -> dict:
        ...

    @abstractmethod
    def _set_params(self, *args, **kwargs):
        ...

    @abstractmethod
    def sign(self, *args, **kwargs):
        ...


class SoftwareOnboardingHeader(BaseOnboardingHeader):
    def __init__(self,
                 reg_code,
                 application_id,
                 signature=None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):

        self._set_params(reg_code, application_id, signature, content_type)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signature):
        self.params["X-Agrirouter-Signature"] = signature

    def _set_params(self, reg_code: str, application_id: str, signature: str, content_type: str):
        header = dict()
        header["Authorization"] = f"Bearer {reg_code}"
        header["Content-Type"] = content_type
        header["X-Agrirouter-ApplicationId"] = application_id
        if signature:
            header["X-Agrirouter-Signature"] = signature

        self.params = header


class CUOnboardingHeader(BaseOnboardingHeader):
    pass
