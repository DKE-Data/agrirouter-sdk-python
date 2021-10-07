import requests

from messaging.result import OutboxResponse


class OutboxService:

    def fetch(self, onboarding_response) -> OutboxResponse:
        response = requests.get(
            url=onboarding_response.get_connection_criteria()["commands"],
            headers={"Content-type": "application/json"},
            # TODO: improve create_certificate_file()
            # verify=create_certificate_file(parameters.get_onboarding_response()),
            # cert=create_certificate_file(parameters.get_onboarding_response()),
        )

        outbox_response = OutboxResponse(status_code=response.status_code)
        outbox_response.json_deserialize(response.json()["contents"])

        return outbox_response

