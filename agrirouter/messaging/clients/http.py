import http.client
import json
import os
import ssl
from urllib.parse import urlparse

from agrirouter.messaging.certification import create_certificate_file_from_pen
from agrirouter.onboarding.dto import ConnectionCriteria
from agrirouter.onboarding.response import SoftwareOnboardingResponse


class HttpClient:

    headers = {"Content-Type": "application/json"}

    def make_connection(self, certificate_file_path: str, onboard_response: SoftwareOnboardingResponse):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(
            certfile=certificate_file_path,
            keyfile=certificate_file_path,
            password=onboard_response.get_authentication().get_secret(),
        )
        connection = http.client.HTTPSConnection(
            host=self.get_host(onboard_response.connection_criteria.get_measures()),
            port=self.get_port(onboard_response.connection_criteria.get_measures()),
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
                    url=urlparse(onboard_response.get_connection_criteria().get_measures()).path,
                    headers=self.headers,
                    body=json.dumps(request_body.json_serialize())
                )
            else:
                connection.request(
                    method=method,
                    url=urlparse(onboard_response.get_connection_criteria().get_measures()).path,
                    headers=self.headers,
                )
            response = connection.getresponse()
        finally:
            os.remove(certificate_file_path)

        return response

    @staticmethod
    def get_host(uri):
        return urlparse(uri).netloc

    @staticmethod
    def get_port(uri):
        return urlparse(uri).port if urlparse(uri).port else None
