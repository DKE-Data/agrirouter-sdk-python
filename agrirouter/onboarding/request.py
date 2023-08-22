from agrirouter.onboarding.headers import SoftwareOnboardingHeader
from agrirouter.onboarding.parameters import OnboardParameters
from agrirouter.onboarding.request_body import SoftwareOnboardingBody
from agrirouter.onboarding.signature import create_signature, verify_signature


class OnboardRequest:
    def __init__(self, header: SoftwareOnboardingHeader, body: SoftwareOnboardingBody):
        self.header = header
        self.body = body

    @classmethod
    def from_onboardparameters(cls, params: OnboardParameters) -> 'OnboardRequest':
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        request_header = SoftwareOnboardingHeader(**header_params)

        return cls(header=request_header, body=request_body)

    def get_data(self):
        return self.body.get_parameters()

    def get_header(self):
        return self.header.get_header()

    def get_body_content(self):
        return self.body.json().replace("\n", "")

    def sign(self, private_key, public_key):
        body = self.get_body_content()
        signature = create_signature(body, private_key)
        verify_signature(body, bytes.fromhex(signature), public_key)
        self.header.sign(signature)

    @property
    def is_signed(self):
        header_has_signature = self.get_header().get("X-Agrirouter-Signature", None)
        if header_has_signature:
            return True
        return False
