import requests

from environments.environmental_services import EnvironmentalService
from onboarding.headers import SoftwareOnboardingHeader, CUOnboardingHeader
from onboarding.parameters import SoftwareOnboardingParameter, BaseOnboardingParameter, RevokingParameter, \
    CUOnboardingParameter
from onboarding.request import SoftwareOnboardingRequest, BaseOnboardingRequest, CUOnboardingRequest
from onboarding.request_body import SoftwareOnboardingBody, CUOnboardingBody
from onboarding.response import SoftwareVerifyOnboardingResponse, SoftwareOnboardingResponse, RevokingResponse, \
    CUOnboardingResponse


class SoftwareOnboarding(EnvironmentalService):

    def _create_request(self, params: BaseOnboardingParameter, url: str) -> SoftwareOnboardingRequest:
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        header_params["request_body"] = request_body.json(new_lines=False)
        request_header = SoftwareOnboardingHeader(**header_params)

        return SoftwareOnboardingRequest(header=request_header, body=request_body, url=url)

    def _perform_request(self, params: BaseOnboardingParameter, url: str) -> requests.Response:
        request = self._create_request(params, url)
        return requests.post(
            url=request.get_url(),
            data=request.get_data(),
            headers=request.get_header()
        )

    def verify(self, params: SoftwareOnboardingParameter) -> SoftwareOnboardingResponse:
        url = self._environment.get_verify_onboard_request_url()
        http_response = self._perform_request(params=params, url=url)

        return SoftwareOnboardingResponse(http_response)

    def onboard(self, params: SoftwareOnboardingParameter) -> SoftwareOnboardingResponse:
        url = self._environment.get_secured_onboard_url()
        http_response = self._perform_request(params=params, url=url)

        return SoftwareOnboardingResponse(http_response)


class CUOnboarding(EnvironmentalService):

    def _create_request(self, params: CUOnboardingParameter, url: str) -> CUOnboardingRequest:
        body_params = params.get_body_params()
        request_body = CUOnboardingBody(**body_params)

        header_params = params.get_header_params()
        header_params["request_body"] = request_body.json(new_lines=False)
        request_header = CUOnboardingHeader(**header_params)

        return CUOnboardingRequest(header=request_header, body=request_body, url=url)

    def _perform_request(self, params: CUOnboardingParameter, url: str) -> requests.Response:
        request = self._create_request(params, url)
        return requests.post(
            url=request.get_url(),
            data=request.get_data(),
            headers=request.get_header()
        )

    def onboard(self, params: CUOnboardingParameter) -> CUOnboardingResponse:
        url = self._environment.get_onboard_url()
        http_response = self._perform_request(params=params, url=url)

        return CUOnboardingResponse(http_response)
