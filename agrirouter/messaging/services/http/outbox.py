import os

import requests

from agrirouter.messaging.clients.http import HttpClient
from agrirouter.messaging.result import OutboxResponse

from agrirouter.messaging.certification import create_certificate_file_from_pen


class OutboxService:

    def __init__(self, on_message_callback, timeout):
        self.client = HttpClient(on_message_callback=on_message_callback, timeout=timeout)

    def fetch(self, onboarding_response) -> OutboxResponse:
        response = self.client.send(
            "GET",
            onboarding_response,
            None
        )

        outbox_response = OutboxResponse(status_code=response.status_code)
        outbox_response.json_deserialize(response.json()["contents"])

        return outbox_response

