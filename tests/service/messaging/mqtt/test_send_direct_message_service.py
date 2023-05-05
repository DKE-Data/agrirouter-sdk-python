import logging
import unittest

import pytest

from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import SendMessageService, SendMessageParameters
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.utils.uuid_util import new_uuid
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import read_onboard_response
from tests.data_provider import DataProvider
from tests.sleeper import Sleeper


class TestSendDirectMessageService(unittest.TestCase):
    """
    Test to send the message to a recipient
    The existing sender and recipient PEM onboard responses are read using OnboardIntegrationService
    """
    _recipient_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH])
    _sender_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH])
    _callback_processed = False
    _log = logging.getLogger(__name__)
    _received_messages = None

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Run the test
        yield

        # Tear down
        if self._received_messages is not None:
            self._log.info("Deleting received messages from the feed to have a clean state: %s",
                           self._received_messages)

    def test_given_valid_message_content_when_sending_message_to_single_recipient_then_the_message_should_be_delivered(
            self):
        """
        Test for sending the valid message content to a single recipient after enabling IMG_PNG capability with
        sender and recipient Open Connection between Recipient and agrirouter is required. The setup between the
        sender and the recipient are done before running the test.
        """

        current_sequence_number = SequenceNumberService.next_seq_nr(
            TestSendDirectMessageService._recipient_onboard_response.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[TestSendDirectMessageService._recipient_onboard_response.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        messaging_service = MqttMessagingService(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
            on_message_callback=TestSendDirectMessageService._on_message_callback)

        send_message_service = SendMessageService(messaging_service=messaging_service)
        send_message_service.send(send_message_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

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
        assert decoded_message.response_envelope.type == 12
        push_notification = decode_details(decoded_message.response_payload.details)
        assert decoded_message.response_envelope.response_code == 200
        assert DataProvider.get_hash(
            push_notification.messages[0].content.value) == DataProvider.get_hash(
            DataProvider.read_base64_encoded_image())

        TestSendDirectMessageService._callback_processed = True
