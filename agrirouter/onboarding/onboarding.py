import requests

from agrirouter.environments.environmental_services import EnvironmentalService
from agrirouter.onboarding.exceptions import RequestNotSigned
from agrirouter.onboarding.headers import SoftwareOnboardingHeader
from agrirouter.onboarding.parameters import OnboardParameters
from agrirouter.onboarding.request import OnboardRequest
from agrirouter.onboarding.request_body import SoftwareOnboardingBody
from agrirouter.onboarding.response import VerificationResponse, OnboardResponse


class SecuredOnboardingService(EnvironmentalService):

    def __init__(self, *args, **kwargs):
        self._public_key = kwargs.pop("public_key")
        self._private_key = kwargs.pop("private_key")
        super(SecuredOnboardingService, self).__init__(*args, **kwargs)

    def _create_request(self, params: OnboardParameters) -> OnboardRequest:
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        request_header = SoftwareOnboardingHeader(**header_params)

        return OnboardRequest(header=request_header, body=request_body)

    def _perform_request(self, params: OnboardParameters, url: str) -> requests.Response:
        request = OnboardRequest.from_onboardparameters(params)
        request.sign(self._private_key, self._public_key)
        if request.is_signed:
            return requests.post(
                url=url,
                data=request.get_body_content(),
                headers=request.get_header()
            )
        raise RequestNotSigned

    def verify(self, params: OnboardParameters) -> VerificationResponse:
        url = self._environment.get_verify_onboard_request_url()
        http_response = self._perform_request(params=params, url=url)

        return VerificationResponse(http_response)

    def onboard(self, params: OnboardParameters) -> OnboardResponse:
        url = self._environment.get_secured_onboard_url()
        http_response = self._perform_request(params=params, url=url)

        return OnboardResponse(http_response)

class OnboardingService(EnvironmentalService):
    def __init__(self, *args, **kwargs):
        super(OnboardingService, self).__init__(*args, **kwargs)

    def _perform_request(self, params: OnboardParameters, url: str) -> requests.Response:
        request = OnboardRequest.from_onboardparameters(params)

        return requests.post(
            url=url,
            data=request.get_body_content(),
            headers=request.get_header()
        )

    def onboard(self, params: OnboardParameters) -> OnboardResponse:
        url = self._environment.get_onboard_url()
        http_response = self._perform_request(params=params, url=url)
        return OnboardResponse(http_response)
