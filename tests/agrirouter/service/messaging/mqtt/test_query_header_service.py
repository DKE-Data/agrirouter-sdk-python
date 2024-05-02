import logging
import unittest
from typing import Optional

import pytest

from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.decode import DecodingService, decode_details
from agrirouter.api.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import FeedDeleteParameters, QueryHeaderParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import SendMessageService, SendMessageParameters, FeedDeleteService, \
    QueryHeaderService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.utc_time_util import max_validity_period, validity_period_for_seconds
from agrirouter.utils.uuid_util import new_uuid
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestQueryHeaderService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _sender_onboard_response = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _received_messages = None

    _callback_for_feed_header_query_processed = False
    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._log.debug("Setup for the test case.")
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
        self._log.debug("Tear down.")
        if self._messaging_service_for_sender:
            self._messaging_service_for_sender.client.disconnect()
        if self._messaging_service_for_recipient:
            self._messaging_service_for_recipient.client.disconnect()

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
            self._log.info("Received message for recipient from the agrirouter: %s",
                           msg.payload.decode())
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 12:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the agrirouter: {str(decoded_details)}")
            push_notification = decode_details(decoded_message.response_payload.details)
            self._received_messages = push_notification.messages[0].header.message_id
            assert decoded_message.response_envelope.response_code == 200
            assert push_notification.messages[0] is not None

            self._received_messages = push_notification.messages[0]

        return _inner_function

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

    def test_header_query_service_when_validity_period_is_specified_should_return_messages_within_the_validity_period(
            self):
        """
        Testing query header service when the validity period is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        validity_period=max_validity_period(),
                                                        )

        self.assertIsNotNone(self._received_messages)
        received_message_ids = [self._received_messages.header.message_id]
        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_header_service_callback(received_message_ids))

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_when_senders_is_specified_should_return_the_header_for_this_sender_id(self):
        """
        Testing query header service when the sender endpoint id is specified
        """
        self._log.info("Testing header query service with specific sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_header_service_callback(None))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[
                                                            self._sender_onboard_response.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_for_specific_message_ids_should_return_the_messages_for_this_specific_message_ids(
            self):
        """
        Testing query header service when specific message id is specified
        """
        self._log.info("Testing header query service with specific message id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self.assertIsNotNone(self._received_messages)
        message_for_message_ids = [self._received_messages.header.message_id]

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._on_query_header_service_callback(message_for_message_ids))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=message_for_message_ids,
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_for_incomplete_attributes_should_return_in_an_error(self):
        """
        Testing query header service when incomplete attributes are passed
        """
        self._log.info("Testing header query service with incomplete attributes")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._incomplete_attributes_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_for_incorrect_message_ids_should_return_empty_message(self):
        """
        Testing query header service when incorrect message ids are specified
        """
        self._log.info("Testing header query service with incorrect message ids")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_for_incorrect_sender_id_should_return_empty_message(self):
        """
        Testing query header service when incorrect sender id is specified
        """
        self._log.info("Testing header query service with incorrect sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._empty_result_in_response_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service_for_recipient)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command(60)

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def test_header_query_service_for_incorrect_validity_period_should_return_empty_message(self):
        """
        Testing query header service when incorrect validity period is specified
        """
        self._log.info("Testing header query service with incorrect validity period")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        _messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                  on_message_callback=self._empty_result_in_response_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        validity_period=validity_period_for_seconds(5),
                                                        )

        query_header_service = QueryHeaderService(_messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False

    def _callback_for_feed_delete(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode Feed Delete Service
            """
            self._log.info("Received message after deleting messages: " + str(msg.payload))
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            delete_details = decode_details(decoded_message.response_payload.details)
            self._log.info("Details for the message removal: " + str(delete_details))
            assert decoded_message.response_envelope.response_code == 201

        return _inner_function

    def _incomplete_attributes_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode query header service response when the attributes are incomplete
            """
            self._log.info("Callback for checking if no messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            details = decode_details(decoded_message.response_payload.details)

            assert decoded_message.response_envelope.response_code == 400
            assert decoded_message.response_envelope.type == 3
            assert details.messages[0].message_code == "VAL_000017"
            assert (details.messages[0].message == "Query does not contain any filtering "
                                                   "criteria: messageIds, senders or validityPeriod. Information "
                                                   "required to process message is missing or malformed.")
            self._callback_for_feed_header_query_processed = True

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
            assert decoded_message.response_envelope.response_code == 204
            self._callback_for_feed_header_query_processed = True

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
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.type != 12:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error(
                    f"Received wrong message from the agrirouter: {str(decoded_details)}")
            push_notification = decode_details(decoded_message.response_payload.details)
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(
                push_notification.messages[0].content.value) == DataProvider.get_hash(
                DataProvider.read_base64_encoded_image())
            self._received_messages = push_notification.messages[0]

        return _inner_function

    def _on_query_header_service_callback(self, message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):
            """
            Callback function for query header service
            """
            self._log.info("Callback for checking if the query header messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            query_header_details = decode_details(decoded_message.response_payload.details)
            self._log.info(f"Query Header Service Details: {query_header_details}")
            assert decoded_message.response_envelope.type == 6
            if query_header_details.feed:
                self._log.info(f"Checking headers for the following message ids: {message_ids}")
                header_query_message_ids = [query_header_details.feed[0].headers[idx].message_id for idx in
                                            range(len(query_header_details.feed[0].headers))]
                if message_ids:
                    for msg_id in message_ids:
                        assert msg_id in header_query_message_ids
                else:
                    assert self._received_messages.header.message_id in header_query_message_ids
            self._callback_for_feed_header_query_processed = True

        return _inner_function
