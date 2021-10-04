from requests import Response


class BaseOnboardingResonse:

    def __init__(self, http_response: Response):
        self.response:  Response = http_response

    @property
    def data(self):
        return self.response.json()

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def text(self):
        return self.response.text


class SoftwareVerifyOnboardingResponse(BaseOnboardingResonse):
    """
    Response from verify request used for Farming Software or Telemetry Platform before onboarding
    """
    pass


class SoftwareOnboardingResponse(BaseOnboardingResonse):
    """
    Response from onboarding request used for Farming Software or Telemetry Platform
    """
    pass


class CUOnboardingResponse(BaseOnboardingResonse):
    """
    Response from onboarding request used for CUs
    """
    pass

