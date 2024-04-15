import json
import logging
from abc import ABC, abstractmethod

from agrirouter.api.exceptions import BadMessagingResult
from agrirouter.messaging.clients.http import HttpClient
from agrirouter.messaging.clients.mqtt import MqttClient
from agrirouter.messaging.messages import Message, EncodedMessage
from agrirouter.messaging.parameters.dto import MessagingParameters
from agrirouter.messaging.parameters.service import MessageParameters
from agrirouter.messaging.request import MessageRequest
from agrirouter.messaging.result import MessagingResult
from agrirouter.onboarding.response import OnboardResponse


class AbstractService:
    """
    Abstract service class for all services.
    """
    _log = logging.getLogger(__name__)

    def __init__(self, messaging_service):
        self.messaging_service = messaging_service

    def send(self, parameters):
        """
        Send a message to the src.
        :param parameters: Parameters for the message.
        """
        self._log.debug("Sending message to the src.")
        messaging_parameters = MessagingParameters(
            onboarding_response=parameters.get_onboarding_response(),
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
        )
        encoded_messages = self.encode(parameters)
        if type(encoded_messages.get_content()) == list:
            messaging_parameters.set_encoded_messages(encoded_messages.get_content())
        else:
            messaging_parameters.set_encoded_messages([encoded_messages.get_content()])

        return self.messaging_service.send(messaging_parameters)

    @staticmethod
    def encode(*args, **kwargs) -> EncodedMessage:
        ...


class AbstractMessagingClient(ABC):

    @staticmethod
    def create_message_request(parameters: MessageParameters) -> MessageRequest:
        messages = []
        for encoded_message in parameters.get_encoded_messages():
            message = Message(encoded_message)
            messages.append(message.json_serialize())
        message_request = MessageRequest(
            parameters.get_onboarding_response().get_sensor_alternate_id(),
            parameters.get_onboarding_response().get_capability_alternate_id(),
            messages
        )
        return message_request

    @abstractmethod
    def send(self, parameters):
        ...


class HttpMessagingService(AbstractMessagingClient):

    def __init__(self):
        self.client = HttpClient()

    def send(self, parameters: MessageParameters) -> MessagingResult:
        request = self.create_message_request(parameters)
        response = self.client.send_measure(parameters.get_onboarding_response(), request)
        if response.status != 200:
            raise BadMessagingResult(f"Messaging Request failed with status code {response.status}")
        result = MessagingResult([parameters.get_application_message_id()])
        return result


class MqttMessagingService(AbstractMessagingClient):

    def __init__(self,
                 onboarding_response: OnboardResponse,
                 on_message_callback: callable = None,
                 client_async: bool = True
                 ):

        self.onboarding_response = onboarding_response
        self.client = MqttClient(
            onboard_response=onboarding_response,
            client_id=onboarding_response.get_connection_criteria().get_client_id(),
            on_message_callback=on_message_callback,
            clean_session=True
        )
        if client_async:
            self.client.connect_async(
                self.onboarding_response.get_connection_criteria().get_host(),
                self.onboarding_response.get_connection_criteria().get_port()
            )
        else:
            self.client.connect(
                self.onboarding_response.get_connection_criteria().get_host(),
                self.onboarding_response.get_connection_criteria().get_port()
            )

    def send(self, parameters, qos: int = 0) -> MessagingResult:
        message_request = self.create_message_request(parameters)
        mqtt_payload = message_request.json_serialize()
        self.client.publish(
            topic=self.onboarding_response.get_connection_criteria().get_measures(),
            payload=json.dumps(mqtt_payload),
            qos=qos
        )
        result = MessagingResult([parameters.get_application_message_id()])
        return result
