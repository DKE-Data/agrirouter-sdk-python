from onboarding.headers import SoftwareOnboardingHeader, BaseOnboardingHeader
from onboarding.request_body import SoftwareOnboardingBody, BaseOnboardingBody
from onboarding.signature import create_signature


class BaseOnboardingRequest:
    def __init__(self, header: BaseOnboardingHeader, body: BaseOnboardingBody, url: str):
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
    def is_signed(self):
        header_has_signature = self.get_header().get("X-Agrirouter-Signature", None)
        if header_has_signature:
            return True
        return False


class SoftwareOnboardingRequest(BaseOnboardingRequest):
    """
    Request must be used to onboard Farming Software or Telemetry Platform
    """
    pass


class CUOnboardingRequest(BaseOnboardingRequest):
    """
    Request must be used to onboard CUs
    """
    pass
