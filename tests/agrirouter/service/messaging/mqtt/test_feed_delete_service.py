import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.api.messages import OutboxMessage
from agrirouter.service.parameter.messaging import FeedDeleteParameters
from agrirouter.service.messaging import MqttMessagingService
from agrirouter.service.messaging import SendMessageService, SendMessageParameters, FeedDeleteService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.util.utc_time_util import UtcTimeUtil
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestFeedDeleteService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _sender_onboard_response = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _received_messages = None

    _callback_for_feed_delete_service_processed = False
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

        # Tear down
        if self._messaging_service_for_sender:
            self._messaging_service_for_sender.client.disconnect()
        if self._messaging_service_for_recipient:
            self._messaging_service_for_recipient.client.disconnect()

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

    def test_delete_messages_for_specified_sender_id_should_delete_the_message_from_the_feed_of_an_endpoint(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for specific sender id")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._callback_for_feed_delete_service())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender_onboard_response.get_sensor_alternate_id()]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_specified_message_id_should_delete_the_message_from_the_feed_of_an_endpoint(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for specific message id.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._callback_for_feed_delete_service())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            message_ids=[self._received_messages.header.message_id]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_given_validity_period_should_delete_the_messages_from_the_feed_of_an_endpoint(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for given validity period.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._callback_for_feed_delete_service())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            validity_period=UtcTimeUtil.max_validity_period()
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_incorrect_message_id_should_return_empty_message(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for incorrect message id.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            message_ids=[UUIDUtil.new_uuid()]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_incorrect_sender_id_should_return_empty_message(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for incorrect sender id.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[UUIDUtil.new_uuid()]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_invalid_validity_period_should_return_empty_message(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for invalid validity period.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            validity_period=UtcTimeUtil.validity_period_for_seconds(5)
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

    def test_delete_messages_for_incomplete_attributes_should_return_in_an_error(self):
        """
        Delete the messages for specified sender id
        """
        self._log.info("Testing feed delete service for incomplete attributes.")

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            validity_period=UtcTimeUtil.validity_period_for_seconds(5)
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_delete_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_feed_delete_service_processed)
        self._callback_for_feed_delete_service_processed = False

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

    def _callback_for_feed_delete_service(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode Feed Delete Service
            """
            self._log.info("Received message after deleting messages: " + str(msg.payload))
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            feed_delete_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info("Details for the message removal: " + str(feed_delete_details))
            message_ids_in_feed = [_message.args['messageId'] for _message in feed_delete_details.messages]
            assert decoded_message.response_envelope.response_code == 201
            assert self._received_messages.header.message_id in message_ids_in_feed
            self._callback_for_feed_delete_service_processed = True

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
            feed_delete_service_for_empty_result = DecodingService.decode_details(
                decoded_message.response_payload.details)
            self._log.info(f"Feed delete details: {feed_delete_service_for_empty_result}")
            assert decoded_message.response_envelope.response_code == 204
            assert feed_delete_service_for_empty_result.messages[0].message_code == "VAL_000208"
            assert feed_delete_service_for_empty_result.messages[0].message == ("Feed does not contain "
                                                                                "any data to be deleted.")
            self._callback_for_feed_delete_service_processed = True

        return _inner_function
