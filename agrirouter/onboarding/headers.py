import logging

from agrirouter.api.enums import ContentTypes, RequestHeaders
from agrirouter.api.exceptions import MissingRegistrationCode


class SoftwareOnboardingHeader:
    def __init__(self,
                 reg_code: str,
                 application_id: str = None,
                 signature: str = None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):
        self._set_params(reg_code, content_type, application_id, signature)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signature: str):
        self.params[RequestHeaders.X_AGRIROUTER_SIGNATURE.value] = signature

    def _set_params(self, reg_code: str, content_type: str, application_id: str, signature: str = None):
        header = dict()

        if reg_code:
            header[RequestHeaders.AUTHORIZATION.value] = f"Bearer {reg_code}"
        else:
            raise MissingRegistrationCode("Registration code is required")

        if content_type:
            header[RequestHeaders.CONTENT_TYPE.value] = content_type
        else:
            logging.warning("Content-Type not set, defaulting to application/json")
            header[RequestHeaders.CONTENT_TYPE.value] = ContentTypes.APPLICATION_JSON.value

        if application_id:
            header[RequestHeaders.X_AGRIROUTER_APPLICATION_ID.value] = application_id

        if signature:
            header[RequestHeaders.X_AGRIROUTER_SIGNATURE.value] = signature if signature else ""

        self.params = header
