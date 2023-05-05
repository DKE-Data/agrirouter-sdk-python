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
    timestamp_before_number_of_seconds
from agrirouter.utils.uuid_util import new_uuid
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.data_provider import DataProvider
from tests.sleeper import Sleeper


class TestQueryHeaderService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = OnboardResponseIntegrationService.read(
        Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH])
    _message_ids_to_clean_up = None
    _log = logging.getLogger(__name__)
    _callback_processed = False

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

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._on_query_header_service_callback(
                                                     None))

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @pytest.mark.skip("No valid fixture for this test")
    def test_header_query_service_when_senders_is_specified_should_return_the_header_for_this_sender_id(self):
        """
        Testing query header service when the sender endpoint id is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._on_query_header_service_callback(
                                                     None))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[
                                                            self._sender_onboard_response.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

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
        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._on_query_header_service_callback(
                                                     message_for_message_ids))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=message_for_message_ids,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incomplete_attributes_should_return_in_an_error(self):
        """
        Testing query header service when incomplete attributes are passed
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._incomplete_attributes_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incorrect_message_ids_should_return_empty_message(self):
        """
        Testing query header service when incorrect message ids are specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._incorrect_ids_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        message_ids=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incorrect_sender_id_should_return_empty_message(self):
        """
        Testing query header service when incorrect sender id is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._incorrect_ids_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        senders=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def test_header_query_service_for_incorrect_validity_period_should_return_empty_message(self):
        """
        Testing query header service when incorrect validity period is specified
        """
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=self._recipient_onboard_response,
                                                 on_message_callback=self._incorrect_ids_callback)

        sent_from = timestamp_before_number_of_seconds(5)
        sent_to = now_as_timestamp()
        validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=self._recipient_onboard_response,
                                                        validity_period=validity_period,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def _feed_delete_service(self, details, onboard_response, messaging_service):
        """
        Feed Delete Service function to delete messages of specific ids
        """
        self._message_ids_to_clean_up = [header.message_id for header in
                                         list(details.feed[0].headers)]

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())
        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number)

        delete_message_parameters.set_message_ids(self._message_ids_to_clean_up)
        delete_message_service = FeedDeleteService(messaging_service)
        delete_message_service.send(delete_message_parameters)

        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @staticmethod
    def _on_query_header_service_callback(message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):

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

                if details.query_metrics.total_messages_in_query > 0:
                    messaging_service = MqttMessagingService(
                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                        on_message_callback=TestQueryHeaderService._on_feed_delete_service_callback)
                    TestQueryHeaderService._feed_delete_service(details=details,
                                                                onboard_response=TestQueryHeaderService._recipient_onboard_response,
                                                                messaging_service=messaging_service)

            TestQueryHeaderService._callback_processed = True

        return _inner_function

    @staticmethod
    def _on_feed_delete_service_callback(client, userdata, msg):
        """
        Callback to decode Feed Delete Service
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        delete_details = decode_details(decoded_message.response_payload.details)
        deleted_message_ids = [idx.args['messageId'] for idx in delete_details.messages]
        assert sorted(TestQueryHeaderService._message_ids_to_clean_up) == sorted(deleted_message_ids)
        TestQueryHeaderService._callback_processed = True

    @staticmethod
    def _incorrect_ids_callback(client, userdata, msg):
        """
        Callback to decode query header service response when incorrect ids are passed as arguments
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        assert decoded_message.response_envelope.response_code == 204
        TestQueryHeaderService._callback_processed = True

    @staticmethod
    def _on_message_capabilities_callback(client, userdata, msg):
        """
        Callback to handle the sender and recipient capabilities
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message()

        if decoded_message.response_envelope.type == 12:
            push_notification = decode_details(decoded_message.response_payload.details)
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(
                push_notification.messages[0].content.value) == DataProvider.get_hash(
                DataProvider.read_base64_encoded_image())

        assert decoded_message.response_envelope.response_code == 201
        TestQueryHeaderService._callback_processed = True

    @staticmethod
    def _incomplete_attributes_callback(client, userdata, msg):
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
        TestQueryHeaderService._callback_processed = True
