from agrirouter.constants.media_types import ContentTypes


class RevokingHeader:
    def __init__(self,
                 application_id,
                 signature=None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):

        self._set_params(application_id, signature, content_type)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signatute):
        self.params["X-Agrirouter-Signature"] = signatute

    def _set_params(self, application_id: str, signature: str, content_type: str):
        header = dict()
        header["Content-Type"] = content_type
        header["X-Agrirouter-ApplicationId"] = application_id
        if signature:
            header["X-Agrirouter-Signature"] = signature

        self.params = header
