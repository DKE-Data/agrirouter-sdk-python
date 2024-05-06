from agrirouter.api.exceptions import CanNotFetchOutboxMessage
from agrirouter.service.client.http import HttpClient
from agrirouter.service.dto.response.messaging import OutboxResponse


class FetchMessageService:

    def __init__(self):
        self.client = HttpClient()

    def fetch(self, onboarding_response) -> OutboxResponse:
        response = self.client.send_command(onboarding_response, None)

        if response.status == 200:
            outbox_response = OutboxResponse(status_code=response.status)
            response_body = response.read()
            outbox_response.json_deserialize(response_body)
        else:
            raise CanNotFetchOutboxMessage(f"Could not fetch messages from outbox. Status code was {response.status}")

        return outbox_response
