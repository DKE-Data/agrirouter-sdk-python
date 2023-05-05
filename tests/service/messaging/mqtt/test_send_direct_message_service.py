import unittest

from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.enums import CapabilityDirectionType
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService, SendMessageService, SendMessageParameters
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.utils.uuid_util import new_uuid
from tests.data.applications import CommunicationUnit
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.data_provider import DataProvider
from tests.sleeper import Sleeper


class SendDirectMessageServiceTest(unittest.TestCase):
    """
    Test to send the message to a recipient
    The existing sender and recipient PEM onboard responses are read using OnboardIntegrationService
    """
    _recipient_onboard_response = OnboardResponseIntegrationService.read(
        Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH])
    _callback_processed = False

    def test_given_valid_message_content_when_sending_message_to_single_recipient_then_the_message_should_be_delivered(
            self):
        """
        Test for sending the valid message content to a single recipient after enabling IMG_PNG capability with
        sender and recipient Open Connection between Recipient and agrirouter is required. The setup between the
        sender and the recipient are done before running the test.
        """
        SendDirectMessageServiceTest._send_capabilities(
            onboard_response=SendDirectMessageServiceTest._recipient_onboard_response,
            callback=SendDirectMessageServiceTest._on_message_callback)

        current_sequence_number = SequenceNumberService.sequence_number_for_endpoint(
            SendDirectMessageServiceTest._recipient_onboard_response.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=SendDirectMessageServiceTest._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[SendDirectMessageServiceTest._recipient_onboard_response.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        messaging_service = MqttMessagingService(
            onboarding_response=SendDirectMessageServiceTest._sender_onboard_response,
            on_message_callback=SendDirectMessageServiceTest._on_message_callback)

        send_message_service = SendMessageService(messaging_service=messaging_service)
        send_message_service.send(send_message_parameters)
        Sleeper.let_agrirouter_process_the_message()

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @staticmethod
    def _on_message_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.type == 12:
            push_notification = decode_details(decoded_message.response_payload.details)
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(
                push_notification.messages[0].content.value) == DataProvider.get_hash(
                DataProvider.read_base64_encoded_image())
        assert decoded_message.response_envelope.response_code == 200 or 201
        SendDirectMessageServiceTest._callback_processed = True

    @staticmethod
    def _send_capabilities(onboard_response, callback):
        """
        Method to enable capabilities via mqtt
        """
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=callback)
        current_sequence_number = SequenceNumberService.sequence_number_for_endpoint(
            onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.ENABLED,
            capability_parameters=[]
        )

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_PNG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.let_agrirouter_process_the_message()
