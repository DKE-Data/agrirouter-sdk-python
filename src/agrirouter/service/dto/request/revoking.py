import json

from agrirouter.api.enums import ContentTypes
from agrirouter.service.signature import SignatureService


class RevokingHeader:
    def __init__(self,
                 application_id,
                 signature=None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):
        self._set_params(application_id, signature, content_type)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signature):
        self.params["X-Agrirouter-Signature"] = signature

    def _set_params(self, application_id: str, signature: str, content_type: str):
        header = dict()
        header["Content-Type"] = content_type
        header["X-Agrirouter-ApplicationId"] = application_id
        if signature:
            header["X-Agrirouter-Signature"] = signature

        self.params = header


class RevokingBody:
    def __init__(self,
                 account_id,
                 endpoint_ids,
                 utc_timestamp,
                 time_zone):
        self._set_params(
            account_id,
            endpoint_ids,
            utc_timestamp,
            time_zone
        )

    def get_parameters(self) -> dict:
        return self.params

    def _set_params(self,
                    account_id,
                    endpoint_ids,
                    utc_timestamp,
                    time_zone
                    ) -> None:
        self.params = {
            "accountId": account_id,
            "endpointIds": endpoint_ids,
            "UTCTimestamp": utc_timestamp,
            "timeZone": time_zone,
        }

    def json(self) -> str:
        return json.dumps(self.get_parameters(), separators=(',', ':'))


class RevokingRequest:

    def __init__(self, header: RevokingHeader, body: RevokingBody, url: str):
        self.header = header
        self.body = body
        self.url = url

    def get_url(self):
        return self.url

    def get_data(self):
        return self.body.get_parameters()

    def get_header(self):
        return self.header.get_header()

    def get_body_content(self):
        return self.body.json().replace("\n", "")

    def sign(self, private_key):
        body = self.get_body_content()
        signature = SignatureService.create_signature(body, private_key)
        self.header.sign(signature)

    @property
    def is_signed(self) -> bool:
        header_has_signature = self.get_header().get("X-Agrirouter-Signature", None)
        if header_has_signature:
            return True
        return False
