import http.client
import json
import os
import ssl

from agrirouter.messaging.certification import create_certificate_file_from_pen
from agrirouter.onboarding.dto import ConnectionCriteria
from agrirouter.onboarding.response import SoftwareOnboardingResponse


class HttpClient:

    headers = {"Content-Type": "application/json"}

    def __init__(
            self,
            on_message_callback: callable,
            timeout=20
    ):
        self.on_message_callback = on_message_callback
        self.timeout = timeout

    @staticmethod
    def make_connection(certificate_file_path: str, onboard_response: SoftwareOnboardingResponse):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(
            certfile=certificate_file_path,
            keyfile=certificate_file_path,
            password=onboard_response.get_authentication().get_secret(),
        )
        connection = http.client.HTTPSConnection(
            host=onboard_response.connection_criteria.get_host(),
            port=onboard_response.connection_criteria.get_port(),
            context=context
        )
        return connection

    def send(self, method: str, onboard_response: SoftwareOnboardingResponse, request_body=None):
        certificate_file_path = create_certificate_file_from_pen(onboard_response)
        try:
            connection = self.make_connection(certificate_file_path, onboard_response)
            if request_body is not None:
                connection.request(
                    method=method,
                    url=onboard_response.get_connection_criteria().get_measures(),
                    headers=self.headers,
                    body=json.dumps(request_body)
                )
            else:
                connection.request(
                    method=method,
                    url=onboard_response.get_connection_criteria().get_measures(),
                    headers=self.headers,
                )
            response = connection.getresponse()
        finally:
            os.remove(certificate_file_path)

        return response

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    def _start_loop(self):
        pass
