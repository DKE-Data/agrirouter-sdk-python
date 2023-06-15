import requests

from agrirouter.environments.environmental_services import EnvironmentalService
#from agrirouter.onboarding.exceptions import RequestNotSigned
from agrirouter.onboarding.headers import SoftwareOnboardingHeader
from agrirouter.onboarding.parameters import SoftwareOnboardingParameter
from agrirouter.onboarding.request import SoftwareOnboardingRequest
from agrirouter.onboarding.request_body import SoftwareOnboardingBody
from agrirouter.onboarding.response import SoftwareVerifyOnboardingResponse, SoftwareOnboardingResponse


class SoftwareOnboarding(EnvironmentalService):

    def __init__(self, *args, **kwargs):
        #self._public_key = kwargs.pop("public_key")
        #self._private_key = kwargs.pop("private_key")
        super(SoftwareOnboarding, self).__init__(*args, **kwargs)

    def _create_request(self, params: SoftwareOnboardingParameter, url: str) -> SoftwareOnboardingRequest:
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        request_header = SoftwareOnboardingHeader(**header_params)

        return SoftwareOnboardingRequest(header=request_header, body=request_body, url=url)

    def _perform_request(self, params: SoftwareOnboardingParameter, url: str) -> requests.Response:
        request = self._create_request(params, url)
        #request.sign(self._private_key, self._public_key)
        #if request.is_signed:
        #    return requests.post(
        #        url=request.get_url(),
        #        data=request.get_body_content(),
        #        headers=request.get_header()
        #    )
        #raise RequestNotSigned
        return requests.post(url=request.get_url(), data=request.get_body_content(), headers=request.get_header())

    def verify(self, params: SoftwareOnboardingParameter) -> SoftwareVerifyOnboardingResponse:
        url = self._environment.get_verify_onboard_request_url()
        http_response = self._perform_request(params=params, url=url)

        return SoftwareVerifyOnboardingResponse(http_response)

    def onboard(self, params: SoftwareOnboardingParameter) -> SoftwareOnboardingResponse:
        url = self._environment.get_onboard_url()
        http_response = self._perform_request(params=params, url=url)

        return SoftwareOnboardingResponse(http_response)
