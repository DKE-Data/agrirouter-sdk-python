import json
import os

import requests

from agrirouter.messaging.clients.http import HttpClient
from agrirouter.messaging.exceptions import OutboxException
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.result import OutboxResponse

from agrirouter.messaging.certification import create_certificate_file_from_pen


class OutboxService:

    def __init__(self):
        self.client = HttpClient()

    def fetch(self, onboarding_response) -> OutboxResponse:
        response = self.client.send_command(onboarding_response, None)

        if response.status == 200:
            outbox_response = OutboxResponse(status_code=response.status)
            response_body = response.read()
            outbox_response.json_deserialize(response_body)
        else:
            raise OutboxException(f"Could not fetch messages from outbox. Status code was {response.status}")

        return outbox_response

