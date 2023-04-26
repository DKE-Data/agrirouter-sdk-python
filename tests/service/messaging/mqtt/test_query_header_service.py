import pytest
from agrirouter import QueryHeaderService, QueryHeaderParameters
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from tests.sleeper import Sleeper
from agrirouter.messaging.enums import CapabilityType
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.utils.utc_time_util import now_as_timestamp_protobuf, protobuf_timestamp_before_number_of_weeks


class TestQueryHeaderService:
    _recipient_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_SENDER_PEM[Identifier.PATH])

    @staticmethod
    def test_header_query_service_when_senders_is_specified():
        """
        Testing Query Header Service when the sender endpoint id is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        senders=[
                                                            TestQueryHeaderService._sender_onboard_response.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_when_validity_period_is_specified():
        """
        Testing Query Header Service when the validity period is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback)

        sent_from = protobuf_timestamp_before_number_of_weeks(4)
        sent_to = now_as_timestamp_protobuf()
        validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        validity_period=validity_period,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_for_specific_message_ids():
        """
        Testing Query Header Service when specific message ids are specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        message_ids=['c74a6a99-3389-42f6-96ba-1a597c5b26f3', 'bb966c18-bfcf-417a-8cd0-2eca6d7b096a'],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_for_incomplete_attributes():
        """
        Testing Query Header Service when specific message ids are specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._incomplete_attributes_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)


    @staticmethod
    def _on_query_header_service_callback(client, userdata, msg):
        """
        Callback to decode Query Header Service response
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message(seconds=5)

        details = decode_details(decoded_message.response_payload.details)

        assert decoded_message.response_envelope.type == 6
        assert len(details.feed[0].headers) > 0
        assert details.feed[0].headers[0].technical_message_type == CapabilityType.IMG_PNG.value

    @staticmethod
    def _incomplete_attributes_callback(client, userdata, msg):
        """
        Callback to decode Query Header Service response
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message(seconds=5)

        details = decode_details(decoded_message.response_payload.details)
        assert decoded_message.response_envelope.response_code == 400
        assert decoded_message.response_envelope.type == 3
        assert details.messages[0].message_code == "VAL_000017"
        assert details.messages[0].message == "Query does not contain any filtering criteria: messageIds, senders or validityPeriod. Information required to process message is missing or malformed."
