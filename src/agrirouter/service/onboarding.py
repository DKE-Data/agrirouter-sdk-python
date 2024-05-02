import requests

from agrirouter.api.env import BaseEnvironment
from agrirouter.api.env import EnvironmentalService
from agrirouter.api.exceptions import UnexpectedErrorDuringOnboarding, RequestNotSigned
from agrirouter.service.dto.request.onboarding import OnboardRequest, SoftwareOnboardingBody, SoftwareOnboardingHeader
from agrirouter.service.dto.response.messaging import VerificationResponse, OnboardResponse
from agrirouter.service.parameter.onboarding import OnboardParameters


class SecuredOnboardingService(EnvironmentalService):

    def __init__(self, env: BaseEnvironment, public_key: str, private_key: str):
        self._public_key = public_key
        self._private_key = private_key
        super(SecuredOnboardingService, self).__init__(env)

    @staticmethod
    def _create_request(params: OnboardParameters) -> OnboardRequest:
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        request_header = SoftwareOnboardingHeader(**header_params)

        return OnboardRequest(header=request_header, body=request_body)

    def _perform_request(self, params: OnboardParameters, url: str) -> requests.Response:
        request = OnboardRequest.from_onboard_parameters(params)
        request.sign(self._private_key, self._public_key)
        if request.is_signed:
            return requests.post(
                url=url,
                data=request.get_body_content(),
                headers=request.get_header()
            )
        raise RequestNotSigned("Request is not signed, cannot perform request.¶")

    def verify(self, params: OnboardParameters) -> VerificationResponse:
        url = self._environment.get_verify_onboard_request_url()
        http_response = self._perform_request(params=params, url=url)

        return VerificationResponse(http_response)

    def onboard(self, params: OnboardParameters) -> OnboardResponse:
        url = self._environment.get_secured_onboard_url()
        http_response = self._perform_request(params=params, url=url)
        if not http_response.ok:
            raise UnexpectedErrorDuringOnboarding(
                f"Onboarding returned HTTP status {http_response.status_code}. Message: {http_response.text}")
        return OnboardResponse(http_response)


class OnboardingService(EnvironmentalService):
    def __init__(self, *args, **kwargs):
        super(OnboardingService, self).__init__(*args, **kwargs)

    @staticmethod
    def _perform_request(params: OnboardParameters, url: str) -> requests.Response:
        request = OnboardRequest.from_onboard_parameters(params)

        return requests.post(
            url=url,
            data=request.get_body_content(),
            headers=request.get_header()
        )

    def onboard(self, params: OnboardParameters) -> OnboardResponse:
        """
        Onboard a device to the agrirouter.
        """
        url = self._environment.get_onboard_url()
        http_response = self._perform_request(params=params, url=url)
        if not http_response.ok:
            raise UnexpectedErrorDuringOnboarding(
                f"Onboarding returned HTTP status {http_response.status_code}. Message: {http_response.text}")
        return OnboardResponse(http_response)
