import requests

from environments.environmental_services import EnvironmentalService


class Revoking(EnvironmentalService):

    def _create_request(self, params: RevokingParameter, url: str) -> RevokingRequest:
        body_params = params.get_body_params()
        request_body = RevokingBody(**body_params)

        header_params = params.get_header_params()
        header_params["request_body"] = request_body.json(new_lines=False)
        request_header = RevokingHeader(**header_params)

        return RevokingRequest(header=request_header, body=request_body, url=url)

    def _perform_request(self, params: RevokingParameter, url: str) -> requests.Response:
        request = self._create_request(params, url)
        return requests.post(
            url=request.get_url(),
            data=request.get_data(),
            headers=request.get_header()
        )

    def revoke(self, params: RevokingParameter) -> RevokingResponse:
        url = self._environment.get_revoke_url()
        http_response = self._perform_request(params=params, url=url)

        return RevokingResponse(http_response)