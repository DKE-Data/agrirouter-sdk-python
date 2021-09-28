from abc import ABC, abstractmethod


class BaseOnboardingResonse(ABC):
    @abstractmethod
    def __init__(self, http_response):
        self.response = http_response


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

