import logging
import unittest
from typing import Optional

import pytest

from agrirouter.api.enums import CapabilityType, TechnicalMessageType
from agrirouter.api.messages import OutboxMessage
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.encoding import EncodingService
from agrirouter.service.messaging.message_sending import FeedDeleteService, SendChunkedMessageService, \
    QueryHeaderService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.onboarding import OnboardResponse
from agrirouter.service.parameter.messaging import FeedDeleteParameters, MessageHeaderParameters, \
    MessagePayloadParameters, QueryHeaderParameters, ChunkedMessageParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestSendAndReceiveChunkedMessages(unittest.TestCase):
    _recipient = None
    _sender = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _callback_for_chunking_feed_header_query_processed = False

    _received_messages = []

    _chunked_message_to_verify = []
    _MAX_CHUNK_SIZE = 1024000

    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._log.debug("Setup for the test case.")
        self._recipient = read_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH])
        self._sender = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])

        self._send_direct_chunked_message()

        # Run the test
        yield

        # Tear down
        self._log.debug("Tear down.")
        if self._messaging_service_for_sender is not None:
            self._messaging_service_for_sender.client.disconnect()
        if self._messaging_service_for_recipient is not None:
            self._messaging_service_for_recipient.client.disconnect()

        self._log.info("Deleting received messages from the feed to have a clean state: %s",
                       self._received_messages)
        self._delete_messages_after_test_run(onboard_response=self._recipient)

    def _delete_messages_after_test_run(self, onboard_response: OnboardResponse):
        """
        Delete the messages after the test run.
        """
        self._log.info("Deleting all existing messages after the test run.")

        self._feed_delete_messaging_service = MqttMessagingService(onboarding_response=onboard_response,
                                                                   on_message_callback=self._callback_for_feed_delete)

        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender.get_sensor_alternate_id()]
        )

        delete_message_service = FeedDeleteService(self._feed_delete_messaging_service)
        delete_message_service.send(delete_message_parameters)

        Sleeper.process_the_command()
        self._feed_delete_messaging_service.client.disconnect()

    def _send_direct_chunked_message(self):
        """
        Test sending direct chunked messages with the push notifications enabled.
        The setup between recipient and sender, like, enabling capabilities and routing has been done prior to running
        this test
        """
        self._log.info("Testing send message service with the specified recipient")

        self._messaging_service_for_sender = MqttMessagingService(
            onboarding_response=self._sender,
            on_message_callback=self._non_checking_callback)

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient,
            on_message_callback=self._callback_to_set_the_received_message_ids)

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient.get_sensor_alternate_id())

        message_header_parameters = MessageHeaderParameters(application_message_id=UUIDUtil.new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            technical_message_type=CapabilityType.IMG_BMP.value,
                                                            recipients=[
                                                                self._recipient.get_sensor_alternate_id()],
                                                            mode=RequestEnvelope.Mode.Value("DIRECT"))

        message_payload_parameters = MessagePayloadParameters(type_url=TechnicalMessageType.EMPTY.value,
                                                              value=DataProvider.read_base64_encoded_large_bmp())

        message_parameter_tuples = EncodingService.chunk_and_base64encode_each_chunk(
            header_parameters=message_header_parameters,
            payload_parameters=message_payload_parameters,
            onboarding_response=self._sender)

        for _tuple in message_parameter_tuples:
            self._chunked_message_to_verify.append(_tuple.message_payload_parameters.get_value())
            assert len(_tuple.message_payload_parameters.get_value()) <= self._MAX_CHUNK_SIZE

        encoded_chunked_messages = EncodingService.encode_chunks_message(
            message_parameter_tuple=message_parameter_tuples)

        chunk_message_parameters = ChunkedMessageParameters(
            onboarding_response=self._sender,
            technical_message_type=CapabilityType.IMG_BMP.value,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[self._recipient.get_sensor_alternate_id()],
            encoded_chunked_messages=encoded_chunked_messages)

        send_chunked_message_service = SendChunkedMessageService(messaging_service=self._messaging_service_for_sender)
        send_chunked_message_service.send(chunk_message_parameters)
        Sleeper.process_the_message()

        self._messaging_service_for_sender.client.disconnect()
        self._messaging_service_for_recipient.client.disconnect()

    def test_receive_chunked_msgs_from_feed_when_sender_id_is_specified_should_return_the_header_for_this_sender_id(
            self):
        """
        Testing query header service when the validity period is specified
        """
        self._log.info("Testing header query service with specific sender id")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient.get_sensor_alternate_id())

        self._messaging_service_for_specified_sender_id = MqttMessagingService(
            onboarding_response=self._recipient,
            on_message_callback=self._on_query_header_service_callback(self._received_messages))

        query_header_parameters = QueryHeaderParameters(application_message_id=UUIDUtil.new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient,
                                                        senders=[
                                                            self._sender.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(
            self._messaging_service_for_specified_sender_id)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_chunking_feed_header_query_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_chunking_feed_header_query_processed)
        self._callback_for_feed_header_query_processed = False
        self._messaging_service_for_specified_sender_id.client.disconnect()

    def _non_checking_callback(self, client, userdata, msg):
        """
        Non checking callback to ensure that the message is processed.
        """
        self._log.info(
            "Received message for the non checking callback, "
            "skipping message and continue to the tests afterwards: " + str(msg.payload))

    def _callback_to_set_the_received_message_ids(self, client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
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
        current_chunked_message = push_notification.messages[0].content.value
        self._received_messages.append(push_notification.messages[0].header.message_id)
        assert decoded_message.response_envelope.response_code == 200
        assert DataProvider.get_hash(current_chunked_message) == DataProvider.get_hash(
            self._chunked_message_to_verify[0])
        self._chunked_message_to_verify.pop(0)
        self._callback_for_chunking_feed_header_query_processed = True

    def _callback_for_feed_delete(self, client, userdata, msg):
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

    def _on_query_header_service_callback(self, message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):
            """
            Callback function for query header service
            """
            self._log.info("Callback for checking if the query header messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            query_header_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info(f"Query Header Service Details: {query_header_details}")
            assert decoded_message.response_envelope.type == 6
            if query_header_details.feed:
                self._log.info(f"Checking headers for the following message ids: {message_ids}")
                header_query_message_ids = [query_header_details.feed[0].headers[idx].message_id for idx in
                                            range(len(query_header_details.feed[0].headers))]
                if message_ids:
                    assert all(msg_id in header_query_message_ids for msg_id in message_ids)
                else:
                    assert self._received_messages[0].header.message_id in header_query_message_ids
            self._callback_for_feed_header_query_processed = True

        return _inner_function
