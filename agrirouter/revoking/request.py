from agrirouter.onboarding.signature import create_signature
from agrirouter.revoking.headers import RevokingHeader
from agrirouter.revoking.request_body import RevokingBody


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

    def sign(self, private_key):
        signature = create_signature(self.body.json(new_lines=False), private_key)
        self.header.sign(signature)

    @property
    def is_signed(self) -> bool:
        header_has_signature = self.get_header().get("X-Agrirouter-Signature", None)
        if header_has_signature:
            return True
        return False

    @property
    def is_valid(self) -> bool:
        if not self.is_signed:
            return False
        signature = self.get_header().get("X-Agrirouter-Signature")
        # return validate_signature(signature)
