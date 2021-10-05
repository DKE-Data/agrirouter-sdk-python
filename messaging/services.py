from abc import ABC, abstractmethod

import requests

from messaging.certification import create_certificate_file
from messaging.messages import Message
from messaging.request import MessageRequest
from messaging.result import MessagingResult


class AbstractClient(ABC):

    def create_message_request(self, parameters) -> MessageRequest:
        messages = []
        for encoded_message in parameters.get_encoded_messages():
            message = Message(encoded_message)
            messages.append(message)
        message_request = MessageRequest(
            parameters.get_sensor_alternate_id(),
            parameters.get_capability_alternate_id(),
            messages
        )
        return message_request

    @abstractmethod
    def send(self, parameters):
        ...


class HttpMessagingClient(AbstractClient):

    def send(self, parameters) -> MessagingResult:
        request = self.create_message_request(parameters)
        response = requests.post(
            url=parameters.get_onboarding_response().get_connection_criteria()["measures"],
            headers={"Content-type": "application/json"},
            data=request.json_serialize(),
            # TODO: improve create_certificate_file()
            # verify=create_certificate_file(parameters.get_onboarding_response()),
            # cert=create_certificate_file(parameters.get_onboarding_response()),
        )
        result = MessagingResult([parameters.get_message_id()])
        return result


class MqttMessagingClient(AbstractClient):

    def send(self, parameters) -> MessagingResult:
        mqtt_payload = self.create_message_request(parameters)
        result = MessagingResult([parameters.get_message_id()])
        return result
