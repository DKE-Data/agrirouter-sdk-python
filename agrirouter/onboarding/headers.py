from agrirouter.constants.media_types import ContentTypes


class SoftwareOnboardingHeader:
    def __init__(self,
                 reg_code,
                 application_id=None,
                 signature=None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):

        self._set_params(reg_code, content_type)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signature: str):
        self.params["X-Agrirouter-Signature"] = signature

    def _set_params(self, reg_code: str, content_type: str):
        header = dict()
        header["Authorization"] = f"Bearer {reg_code}"
        header["Content-Type"] = content_type
        #header["X-Agrirouter-ApplicationId"] = application_id
        #header["X-Agrirouter-Signature"] = signature if signature else ""

        self.params = header
