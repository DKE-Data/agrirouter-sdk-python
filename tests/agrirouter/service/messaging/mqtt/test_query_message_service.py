import logging
import unittest
from typing import Optional

import pytest

from src.agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from src.agrirouter.messaging.decode import decode_response, decode_details
from src.agrirouter.api.enums import CapabilityType
from src.agrirouter.messaging.messages import OutboxMessage
from src.agrirouter.messaging.parameters.service import FeedDeleteParameters, QueryMessageParameters
from src.agrirouter.messaging.services.commons import MqttMessagingService
from src.agrirouter.messaging.services.messaging import SendMessageService, SendMessageParameters, FeedDeleteService, \
    QueryMessagesService
from src.agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from src.agrirouter.onboarding.response import OnboardResponse
from src.agrirouter.utils.utc_time_util import max_validity_period, validity_period_for_seconds
from src.agrirouter.utils.uuid_util import new_uuid
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestQueryMessageServiceForSingleMessage(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _sender_onboard_response = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _received_messages = None

    _callback_for_feed_message_query_processed = False
    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._log.info("Setup.")
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

        # Tear down
        self._log.info("Tear down")
        self._log.info("Deleting received messages from the feed to have a clean state: %s",
                       self._received_messages)
        self._delete_messages_after_test_run(onboard_response=self._recipient_onboard_response)

    def send_message_before_the_test_run(self):
        """
            Send a valid message content to a single recipient after enabling IMG_PNG capability with
            sender and recipient. Open Connection between Recipient and src is required. The setup between the
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
            application_message_id=new_uuid(),
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
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender_onboard_response.get_sensor_alternate_id()]
        )

        delete_message_service = FeedDeleteService(self._messaging_service_for_recipient)
        delete_message_service.send(delete_message_parameters)

        Sleeper.process_the_command()
        self._messaging_service_for_recipient.client.disconnect()

    def test_message_query_service_when_validity_period_is_specified_should_return_the_message_for_this_validity_period(
            self):
        """
        Testing query message service when the validation period is specified
        """
        self._log.info("Testing message query service with specific sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_message_service_callback([self._received_messages.header.message_id]))

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          validity_period=max_validity_period(),
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def test_message_query_service_when_sender_is_specified_should_return_the_message_for_this_sender_id(self):
        """
        Testing query message service when the sender endpoint id is specified
        """
        self._log.info("Testing message query service with specific sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_message_service_callback(None))

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          senders=[
                                                              self._sender_onboard_response.get_sensor_alternate_id()],
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def test_message_query_service_when_message_id_is_specified_should_return_the_message_for_this_message_id(self):
        """
        Testing query message service when the message id is specified
        """
        self._log.info("Testing message query service with specific sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_message_service_callback([self._received_messages.header.message_id]))

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          message_ids=[
                                                              self._received_messages.header.message_id],
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def test_query_message_service_for_incorrect_message_ids_should_return_empty_message(self):
        """
        Testing query message service when incorrect message ids are specified
        """
        self._log.info("Testing query message service with incorrect message ids")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          message_ids=[new_uuid()],
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def test_query_message_service_for_incorrect_sender_ids_should_return_empty_message(self):
        """
        Testing query message service when incorrect sender id is specified
        """
        self._log.info("Testing query message service with incorrect message ids")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          senders=[new_uuid()],
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def test_query_message_service_for_incorrect_validity_period_should_return_empty_message(self):
        """
        Testing query message service when incorrect message ids are specified
        """
        self._log.info("Testing query message service with invalid validation period")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        query_message_parameters = QueryMessageParameters(application_message_id=new_uuid(),
                                                          application_message_seq_no=current_sequence_number,
                                                          onboarding_response=self._recipient_onboard_response,
                                                          validity_period=validity_period_for_seconds(seconds=5),
                                                          )

        query_message_service = QueryMessagesService(self._messaging_service_for_recipient)
        query_message_service.send(query_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_message_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_message_query_processed)
        self._callback_for_feed_message_query_processed = False

    def _non_checking_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Non checking callback to ensure that the message is processed.
            """
            self._log.info("Received message for the non checking callback, "
                           "skipping message and continue to the tests afterwards: " + str(msg.payload))

        return _inner_function

    def _callback_to_set_the_received_message_ids(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to set the received message ids
            """
            self._log.info("Received message for recipient from the src: %s",
                           msg.payload.decode())
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 12:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the src: {str(decoded_details)}")
            push_notification = decode_details(decoded_message.response_payload.details)
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
            decoded_message = decode_response(outbox_message.command.message.encode())
            delete_details = decode_details(decoded_message.response_payload.details)
            self._log.info("Details for the message removal: " + str(delete_details))
            assert decoded_message.response_envelope.response_code == 201

        return _inner_function

    def _on_query_message_service_callback(self, message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):
            """
            Callback function for query message service
            """
            self._log.info("Callback for checking if the content from query messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            query_message_details = decode_details(decoded_message.response_payload.details)
            self._log.info(f"Query Message Service Details: {query_message_details}")
            assert decoded_message.response_envelope.type == 7
            message_query_message_ids = [query_message_details.messages[idx].header.message_id for idx in
                                         range(len(query_message_details.messages))]
            if message_ids:
                for _msg_idx, _msg_id in enumerate(message_ids):
                    if _msg_id in message_query_message_ids:
                        assert DataProvider.get_hash(
                            query_message_details.messages[_msg_idx].content.value) == DataProvider.get_hash(
                            self._received_messages.content.value)
            else:
                for _idx, _message in enumerate(query_message_details.messages):
                    if self._received_messages.header.message_id == _message.header.message_id:
                        assert DataProvider.get_hash(_message.content.value) == DataProvider.get_hash(
                            self._received_messages.content.value)

            self._callback_for_feed_message_query_processed = True

        return _inner_function

    def _empty_result_in_response_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode query header service response when incorrect ids are passed as arguments
            """
            self._log.info("Callback for checking if no messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            assert decoded_message.response_envelope.response_code == 204
            self._callback_for_feed_message_query_processed = True

        return _inner_function
