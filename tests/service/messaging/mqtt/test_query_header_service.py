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


class TestQueryHeaderService:

    _recipient_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_SENDER_PEM[Identifier.PATH])


    @staticmethod
    def test_query_message_headers_for_the_existing_message_within_the_feed_of_an_endpoint():
        """
        Testing Message Headers of the existing messages within the feed of an endpoint
        """
        TestQueryHeaderService._header_query_service(callback=TestQueryHeaderService._on_query_header_service_callback)


    @staticmethod
    def _header_query_service(callback):
        """
        Query header Service Function with the callback as an argument
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        senders=[
                                                            TestQueryHeaderService._sender_onboard_response.get_sensor_alternate_id()]
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
