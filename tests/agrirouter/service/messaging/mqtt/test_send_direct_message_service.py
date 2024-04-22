import logging
import unittest

import pytest

from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.api.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import FeedDeleteParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import SendMessageService, SendMessageParameters, FeedDeleteService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.uuid_util import new_uuid
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestSendDirectMessageService(unittest.TestCase):
    """
    Test to send the message to a recipient
    The existing sender and recipient PEM onboard responses are read using OnboardIntegrationService
    """
    _sender = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])
    _recipient = read_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH])

    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None

    _callback_for_sender_processed = False
    _callback_for_recipient_processed = False

    _log = logging.getLogger(__name__)
    _received_messages = None

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._messaging_service_for_sender = MqttMessagingService(
            onboarding_response=self._sender,
            on_message_callback=self._callback_for_sender())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient,
            on_message_callback=self._callback_for_recipient())

        # Run the test
        yield

        # Tear down
        self._messaging_service_for_sender.client.disconnect()
        self._messaging_service_for_recipient.client.disconnect()

        self._log.info("Deleting received messages from the feed to have a clean state: %s",
                       self._received_messages)
        self.delete_all_messages_within_the_feed(onboard_response=self._recipient)

    def test_given_valid_message_content_when_sending_message_to_single_recipient_then_the_message_should_be_delivered(
            self):
        """
        Test for sending the valid message content to a single recipient after enabling IMG_PNG capability with
        sender and recipient Open Connection between Recipient and agrirouter is required. The setup between the
        sender and the recipient are done before running the test.
        """

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._sender.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=self._sender,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[self._recipient.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        send_message_service = SendMessageService(messaging_service=self._messaging_service_for_sender)
        send_message_service.send(send_message_parameters)
        Sleeper.process_the_message()

        if not self._callback_for_sender_processed:
            self._log.error(
                "Either the callback for the sender was not processed "
                "in time or there was an error during the checks.")

        if not self._callback_for_recipient_processed:
            self._log.error(
                "Either the callback for the recipient was not processed "
                "in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_sender_processed)
        self.assertTrue(self._callback_for_recipient_processed)

    def _callback_for_sender(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to handle the incoming messages from the MQTT broker
            """
            self._log.info("Received message for sender from the agrirouter: %s",
                           msg.payload.decode())
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 1:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the agrirouter: {str(decoded_details)}")
            assert decoded_message.response_envelope.response_code == 201
            self._callback_for_sender_processed = True

        return _inner_function

    def _callback_for_recipient(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to handle the incoming messages from the MQTT broker
            """
            self._log.info("Received message for recipient from the agrirouter: %s",
                           msg.payload.decode())
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 12:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the agrirouter: {str(decoded_details)}")
            push_notification = decode_details(decoded_message.response_payload.details)
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(
                push_notification.messages[0].content.value) == DataProvider.get_hash(
                DataProvider.read_base64_encoded_image())

            self._callback_for_recipient_processed = True

        return _inner_function

    def delete_all_messages_within_the_feed(self, onboard_response: OnboardResponse):
        """
        Delete all messages within the feed.
        """
        logging.getLogger(__name__).info(
            f"Delete all messages within the feed for endpoint '{self._recipient.get_sensor_alternate_id()}'.")
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=self._callback_for_feed_delete())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender.get_sensor_alternate_id()]
        )

        feed_delete_service = FeedDeleteService(messaging_service)
        feed_delete_service.send(delete_message_parameters)

        Sleeper.process_the_command()

    def _callback_for_feed_delete(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode Feed Delete Service
            """
            self._log.info("Received message after deleting messages: " + str(msg.payload))
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            delete_details = decode_details(decoded_message.response_payload.details)
            self._log.info("Details for the message removal: " + str(delete_details))
            assert decoded_message.response_envelope.response_code == 201

        return _inner_function
