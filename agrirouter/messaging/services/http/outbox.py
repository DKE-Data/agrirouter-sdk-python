import requests

from agrirouter.messaging.result import OutboxResponse

from agrirouter.messaging.certification import create_certificate_file


class OutboxService:

    def fetch(self, onboarding_response) -> OutboxResponse:
        response = requests.get(
            url=onboarding_response.get_connection_criteria().get_commands(),
            headers={"Content-type": "application/json"},
            cert=(
                create_certificate_file(onboarding_response),
                onboarding_response.get_authentication().get_secret()
            ),
        )

        outbox_response = OutboxResponse(status_code=response.status_code)
        outbox_response.json_deserialize(response.json()["contents"])

        return outbox_response

