import http.client
import json
import os
import ssl
from urllib.parse import urlparse

from agrirouter.service.certification import CertificationService
from agrirouter.service.dto.response.messaging import OnboardResponse


class HttpClient:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def make_connection(self, certificate_file_path: str, uri: str, onboard_response: OnboardResponse):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(
            certfile=certificate_file_path,
            keyfile=certificate_file_path,
            password=onboard_response.get_authentication().get_secret(),
        )
        connection = http.client.HTTPSConnection(
            host=self.get_host(uri),
            port=self.get_port(uri),
            context=context
        )
        return connection

    def send_measure(self, onboard_response: OnboardResponse, request_body=None):
        return self.send(
            method="POST",
            uri=onboard_response.get_connection_criteria().get_measures(),
            onboard_response=onboard_response,
            request_body=request_body
        )

    def send_command(self, onboard_response: OnboardResponse, request_body=None):
        return self.send(
            method="GET",
            uri=onboard_response.get_connection_criteria().get_commands(),
            onboard_response=onboard_response,
            request_body=request_body
        )

    def send(self, method: str, uri: str, onboard_response: OnboardResponse, request_body=None):
        certificate_file_path = CertificationService.create_certificate_file_from_pen(onboard_response)
        try:
            connection = self.make_connection(certificate_file_path, uri, onboard_response)
            if request_body is not None:
                connection.request(
                    method=method,
                    url=self.get_path(uri),
                    headers=self.headers,
                    body=json.dumps(request_body.json_serialize())
                )
            else:
                connection.request(
                    method=method,
                    url=self.get_path(uri),
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

    @staticmethod
    def get_path(uri):
        return urlparse(uri).path
