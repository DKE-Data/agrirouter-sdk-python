from onboarding.headers import SoftwareOnboardingHeader, BaseOnboardingHeader
from onboarding.request_body import SoftwareOnboardingBody, BaseOnboardingBody


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

    def sign(self):
        """
        TODO: add here create_signature
        :return:
        """
        signature = ...     # create signature
        self.header.sign(signature)
        pass

    @property
    def is_signed(self):
        header_has_signature = self.get_header().get("X-Agrirouter-Signature", None)
        if header_has_signature:
            return True
        return False

    @property
    def is_valid(self):
        if not self.is_signed:
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
