import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType, TechnicalMessageType
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.decode import DecodingService
from agrirouter.messaging.encode import chunk_and_base64encode_each_chunk, encode_chunks_message
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.dto import ChunkedMessageParameters
from agrirouter.messaging.parameters.service import FeedDeleteParameters, MessageHeaderParameters, \
    MessagePayloadParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import FeedDeleteService, SendChunkedMessageService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.uuid_util import new_uuid
from tests.agrirouter.common.data_provider import DataProvider
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestSendAndReceiveChunkedMessages(unittest.TestCase):
    _recipient = None
    _sender = None
    _messaging_service_for_sender = None
    _messaging_service_for_recipient = None
    _received_messages = None
    _callback_for_chunking_message_processed = False

    _chunked_message_to_verify = []
    _MAX_CHUNK_SIZE = 1024000

    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._log.debug("Setup for the test case.")
        self._recipient = read_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH])
        self._sender = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])

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
                                                                   on_message_callback=self._callback_for_feed_delete())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            senders=[self._sender.get_sensor_alternate_id()]
        )

        delete_message_service = FeedDeleteService(self._feed_delete_messaging_service)
        delete_message_service.send(delete_message_parameters)

        Sleeper.process_the_command()
        self._feed_delete_messaging_service.client.disconnect()

    def test_send_direct_chunked_message_with_valid_recipient_should_return_the_valid_chunked_message_content(self):
        """
        Test sending direct chunked messages with the push notifications enabled.
        The setup between recipient and sender, like, enabling capabilities and routing has been done prior to running
        this test
        """
        self._log.info("Testing send message service with the specified recipient")

        self._messaging_service_for_sender = MqttMessagingService(
            onboarding_response=self._sender,
            on_message_callback=self._non_checking_callback())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient,
            on_message_callback=self._callback_to_set_the_received_message_ids())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient.get_sensor_alternate_id())

        message_header_parameters = MessageHeaderParameters(application_message_id=new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            technical_message_type=CapabilityType.IMG_BMP.value,
                                                            recipients=[
                                                                self._recipient.get_sensor_alternate_id()],
                                                            mode=RequestEnvelope.Mode.Value("DIRECT"))

        message_payload_parameters = MessagePayloadParameters(type_url=TechnicalMessageType.EMPTY.value,
                                                              value=DataProvider.read_base64_encoded_large_bmp())

        message_parameter_tuples = chunk_and_base64encode_each_chunk(header_parameters=message_header_parameters,
                                                                     payload_parameters=message_payload_parameters,
                                                                     onboarding_response=self._sender)

        for _tuple in message_parameter_tuples:
            self._chunked_message_to_verify.append(_tuple.message_payload_parameters.get_value())
            assert len(_tuple.message_payload_parameters.get_value()) <= self._MAX_CHUNK_SIZE

        encoded_chunked_messages = encode_chunks_message(message_parameter_tuple=message_parameter_tuples)

        if not len(encoded_chunked_messages) == 10:
            self._log.error("Number of chunks not as expected. Check the data being chunked. ")

        chunk_message_parameters = ChunkedMessageParameters(
            onboarding_response=self._sender,
            technical_message_type=CapabilityType.IMG_BMP.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[self._recipient.get_sensor_alternate_id()],
            encoded_chunked_messages=encoded_chunked_messages)

        send_chunked_message_service = SendChunkedMessageService(messaging_service=self._messaging_service_for_sender)
        send_chunked_message_service.send(chunk_message_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_chunking_message_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_for_chunking_message_processed)
        self._callback_for_chunking_message_processed = False

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
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(current_chunked_message) == DataProvider.get_hash(
                self._chunked_message_to_verify[0])
            self._chunked_message_to_verify.pop(0)
            self._callback_for_chunking_message_processed = True

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
