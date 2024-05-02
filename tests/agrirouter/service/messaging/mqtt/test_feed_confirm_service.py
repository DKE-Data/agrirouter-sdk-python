import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType
from agrirouter.api.messages import OutboxMessage
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.service.dto.messaging import SendMessageParameters
from agrirouter.service.messaging import MqttMessagingService
from agrirouter.service.messaging import SendMessageService, FeedDeleteService, FeedConfirmService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.onboarding import OnboardResponse
from agrirouter.service.parameter.messaging import FeedDeleteParameters, FeedConfirmParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestFeedConfirmService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _sender_onboard_response = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _received_messages = None

    _callback_for_feed_confirm_service_processed = False
    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._recipient_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH])
        self._sender_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])

        self.send_message_before_the_test_run()

        if self._messaging_service_for_sender:
            self._messaging_service_for_sender.client.disconnect()
        if self._messaging_service_for_recipient:
            self._messaging_service_for_recipient.client.disconnect()

        # Run the test
        yield

        if self._messaging_service_for_sender:
            self._messaging_service_for_sender.client.disconnect()
        if self._messaging_service_for_recipient:
            self._messaging_service_for_recipient.client.disconnect()

        # Tear Down
        self._log.info("Deleting received messages from the feed to have a clean state: %s",
                       self._received_messages)
        self._delete_messages_after_test_run(onboard_response=self._recipient_onboard_response)

    def send_message_before_the_test_run(self):
        """
            Send a valid message content to a single recipient after enabling IMG_PNG capability with
            sender and recipient. Open Connection between Recipient and agrirouter is required. The setup between the
            sender and the recipient has been done before running the test.
        """
        self._log.info("Sending a message before the test run")

        self._messaging_service_for_sender = MqttMessagingService(
            onboarding_response=self._sender_onboard_response,
            on_message_callback=self._non_checking_callback())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._callback_to_set_the_received_message_ids())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._sender_onboard_response.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=self._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[self._recipient_onboard_response.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        send_message_service = SendMessageService(messaging_service=self._messaging_service_for_sender)
        send_message_service.send(send_message_parameters)
        Sleeper.process_the_message()

        self._messaging_service_for_sender.client.disconnect()
        self._messaging_service_for_recipient.client.disconnect()

    def _delete_messages_after_test_run(self, onboard_response: OnboardResponse):
        """
        Delete the messages after the test run.
        """
        self._log.info("Deleting all existing messages after the test run.")

        self._messaging_service_for_recipient = MqttMessagingService(onboard_response, self._callback_for_feed_delete())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender_onboard_response.get_sensor_alternate_id()]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)

        Sleeper.process_the_command()
        self._messaging_service_for_recipient.client.disconnect()

    def test_feed_confirm_service_for_valid_message_id_should_return_the_message_for_this_message_id(self):
        """
        Testing feed confirm service when the message id is specified
        """
        self._log.info("Testing feed confirm service with specific message id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._feed_confirm_service_callback())

        feed_confirm_parameters = FeedConfirmParameters(message_ids=[self._received_messages.header.message_id],
                                                        application_message_id=UUIDUtil.new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response)

        feed_confirm_service = FeedConfirmService(self._messaging_service_for_recipient)
        feed_confirm_service.send(feed_confirm_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_confirm_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_confirm_service_processed)
        self._callback_for_feed_confirm_service_processed = False

    def test_feed_confirm_service_for_incorrect_message_id_should_return_an_empty_message(self):
        """
        Testing feed confirm service when incorrect message id is specified
        """
        self._log.info("Testing feed confirm service with specific message id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        feed_confirm_parameters = FeedConfirmParameters(message_ids=[UUIDUtil.new_uuid()],
                                                        application_message_id=UUIDUtil.new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response)

        feed_confirm_service = FeedConfirmService(self._messaging_service_for_recipient)
        feed_confirm_service.send(feed_confirm_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_confirm_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_confirm_service_processed)
        self._callback_for_feed_confirm_service_processed = False

    def test_feed_confirm_service_for_multiple_invalid_message_ids_should_return_empty_messages(self):
        """
        Testing feed confirm service when incorrect message id is specified
        """
        self._log.info("Testing feed confirm service with specific message id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        feed_confirm_parameters = FeedConfirmParameters(message_ids=[UUIDUtil.new_uuid(), UUIDUtil.new_uuid()],
                                                        application_message_id=UUIDUtil.new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response)

        feed_confirm_service = FeedConfirmService(self._messaging_service_for_recipient)
        feed_confirm_service.send(feed_confirm_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_confirm_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_confirm_service_processed)
        self._callback_for_feed_confirm_service_processed = False

    def _non_checking_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Non checking callback to ensure that the message is processed.
            """
            self._log.info(
                "Received message for the non checking callback, "
                "skipping message and continue to the tests afterwards: " + str(msg.payload))

        return _inner_function

    def _callback_to_set_the_received_message_ids(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to set the received message ids
            """
            self._log.info("Received message for recipient from the agrirouter: %s",
                           msg.payload.decode())
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 12:
                decoded_details = DecodingService.decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the agrirouter: {str(decoded_details)}")
            push_notification = DecodingService.decode_details(decoded_message.response_payload.details)
            assert decoded_message.response_envelope.response_code == 200
            self._received_messages = push_notification.messages[0]

        return _inner_function

    def _callback_for_feed_delete(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode Feed Delete Service
            """
            self._log.info("Received message after deleting messages: " + str(msg.payload))
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            delete_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info("Details for the message removal: " + str(delete_details))
            assert decoded_message.response_envelope.response_code == 201

        return _inner_function

    def _feed_confirm_service_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback function for feed confirm service
            """
            self._log.info("Callback for checking if the feed confirm messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            feed_confirm_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info(f"Feed Confirm Service Details: {feed_confirm_details}")
            assert decoded_message.response_envelope.response_code == 200
            assert all(
                self._received_messages.header.message_id in feed_confirm_details.messages[idx].args['messageId'] for
                idx in range(len(feed_confirm_details.messages)))
            self._callback_for_feed_confirm_service_processed = True

        return _inner_function

    def _empty_result_in_response_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode query header service response when incorrect ids are passed as arguments
            """
            self._log.info("Callback for checking if no messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            feed_confirm_details_for_empty_messages = DecodingService.decode_details(
                decoded_message.response_payload.details)
            self._log.info(f"Feed confirm details for empty messages: {feed_confirm_details_for_empty_messages}")
            assert decoded_message.response_envelope.response_code == 200
            for _message in feed_confirm_details_for_empty_messages.messages:
                assert _message.message_code == "VAL_000205"
                assert self._received_messages.header.message_id != _message.args['messageId']

            self._callback_for_feed_confirm_service_processed = True

        return _inner_function
