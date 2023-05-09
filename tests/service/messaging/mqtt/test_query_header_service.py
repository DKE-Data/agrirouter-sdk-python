import logging
import unittest
from typing import Optional

import pytest

from agrirouter import QueryHeaderService, QueryHeaderParameters, FeedDeleteService, FeedDeleteParameters
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.utils.utc_time_util import now_as_timestamp, timestamp_before_number_of_weeks, \
    timestamp_before_number_of_seconds, max_validity_period
from agrirouter.utils.uuid_util import new_uuid
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import read_onboard_response
from tests.sleeper import Sleeper


class TestQueryHeaderService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _sender_onboard_response = None
    _messaging_service = None
    _callback_processed = False
    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._recipient_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH])
        self._sender_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH])

        yield

        if self._messaging_service is not None:
            self._messaging_service.client.disconnect()
        self._delete_messages_after_test_run()

    def _delete_messages_after_test_run(self):
        """
        Delete the messages after the test run.
        """
        self._log.info("Deleting all existing messages after the test run.")

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._delete_messages_callback())

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=self._recipient_onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number)

        delete_message_parameters.set_validity_period(max_validity_period())
        delete_message_service = FeedDeleteService(self._messaging_service)
        delete_message_service.send(delete_message_parameters)

        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

        self._messaging_service.client.disconnect()

    def _delete_messages_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to check if the messages were deleted.
            """
            self._log.info("Callback for checking if the messages were deleted.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            details = decode_details(decoded_message.response_payload.details)
            self._log.info("Delete details: %s", details)
            self._callback_processed = True

        return _inner_function

    @pytest.mark.skip("No valid fixture for this test")
    def test_header_query_service_when_validity_period_is_specified_should_return_messages_within_the_validity_period(
            self):
        """
        Testing query header service when the validity period is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        sent_from = timestamp_before_number_of_weeks(4)
        sent_to = now_as_timestamp()
        validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        validity_period=validity_period,
                                                        )

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._on_query_header_service_callback(None))

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @pytest.mark.skip("No valid fixture for this test")
    def test_header_query_service_when_senders_is_specified_should_return_the_header_for_this_sender_id(self):
        """
        Testing query header service when the sender endpoint id is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._on_query_header_service_callback(
                                                           None))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[
                                                            self._sender_onboard_response.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @pytest.mark.skip("No valid fixture for this test")
    def test_header_query_service_for_specific_message_ids_should_return_the_messages_for_this_specific_message_ids(
            self):
        """
        Testing query header service when specific message ids are specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        message_for_message_ids = ['33270996-13f6-4127-a9a9-0a6e09b7810b', 'c81b46bb-deeb-4257-bb01-5dc4bb789d24']
        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._on_query_header_service_callback(
                                                           message_for_message_ids))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=message_for_message_ids,
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incomplete_attributes_should_return_in_an_error(self):
        """
        Testing query header service when incomplete attributes are passed
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._incomplete_attributes_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def _incomplete_attributes_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode query header service response when the attributes are incomplete
            """
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            details = decode_details(decoded_message.response_payload.details)

            assert decoded_message.response_envelope.response_code == 400
            assert decoded_message.response_envelope.type == 3
            assert details.messages[0].message_code == "VAL_000017"
            assert details.messages[
                       0].message == "Query does not contain any filtering criteria: messageIds, senders or " \
                                     "validityPeriod. Information required to process message is missing or malformed."
            self._callback_processed = True

        return _inner_function

    def test_header_query_service_for_incorrect_message_ids_should_return_empty_message(self):
        """
        Testing query header service when incorrect message ids are specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._empty_result_in_response_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incorrect_sender_id_should_return_empty_message(self):
        """
        Testing query header service when incorrect sender id is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._empty_result_in_response_callback())

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incorrect_validity_period_should_return_empty_message(self):
        """
        Testing query header service when incorrect validity period is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                       on_message_callback=self._empty_result_in_response_callback())

        sent_from = timestamp_before_number_of_seconds(5)
        sent_to = now_as_timestamp()
        validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        validity_period=validity_period,
                                                        )

        query_header_service = QueryHeaderService(self._messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def _empty_result_in_response_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode query header service response when incorrect ids are passed as arguments
            """
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            assert decoded_message.response_envelope.response_code == 204
            self._callback_processed = True

        return _inner_function

    def _on_query_header_service_callback(self, message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):
            """
            Callback function for query header service
            """
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            details = decode_details(decoded_message.response_payload.details)

            assert decoded_message.response_envelope.type == 6

            if details.feed:
                header_query_message_ids = [details.feed[0].headers[idx].message_id for idx in
                                            range(len(details.feed[0].headers))]

                if message_ids:
                    assert sorted(header_query_message_ids) == sorted(message_ids)

                assert details.feed[0].headers[0].technical_message_type == CapabilityType.IMG_PNG.value

            self._callback_processed = True

        return _inner_function
