import pytest
from agrirouter import QueryHeaderService, QueryHeaderParameters, FeedDeleteService, FeedDeleteParameters
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from tests.sleeper import Sleeper
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.utils.utc_time_util import now_as_timestamp_protobuf, protobuf_timestamp_before_number_of_weeks, \
    protobuf_timestamp_before_few_seconds
from agrirouter.messaging.services.messaging import CapabilitiesService, SendMessageService, SendMessageParameters
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from tests.data.applications import CommunicationUnit
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from tests.data_provider import DataProvider
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from typing import Optional


class TestQueryHeaderService:
    _recipient_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_SENDER_PEM[Identifier.PATH])
    _message_ids_to_clean_up = None

    @staticmethod
    def _enable_capabilities_via_mqtt(onboard_response, callback):
        """
        Method to enable capabilities via mqtt
        """
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.ENABLED,
            capability_parameters=[]
        )

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_PNG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    @pytest.mark.skip('The setup for the sender and recipient was already done')
    def test_clean_setup_for_recipient_and_sender():
        """
        The sender and recipient capabilities to be set via mqtt and the message is sent and received by the recipient using
        SendMessageService
        This is ignored for this test scenario since the routing between the current recipient and sender has been done
        before running the tests
        """
        TestQueryHeaderService._enable_capabilities_via_mqtt(
            onboard_response=TestQueryHeaderService._recipient_onboard_response,
            callback=TestQueryHeaderService._on_message_capabilities_callback)

        TestQueryHeaderService._enable_capabilities_via_mqtt(
            onboard_response=TestQueryHeaderService._sender_onboard_response,
            callback=TestQueryHeaderService._on_message_capabilities_callback)

        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=TestQueryHeaderService._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        messaging_service = MqttMessagingService(
            onboarding_response=TestQueryHeaderService._sender_onboard_response,
            on_message_callback=TestQueryHeaderService._on_message_capabilities_callback)

        send_message_service = SendMessageService(messaging_service=messaging_service)
        send_message_service.send(send_message_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_when_validity_period_is_specified_should_return_messages_within_the_validity_period():
        """
        Testing Query Header Service when the validity period is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        sent_from = protobuf_timestamp_before_number_of_weeks(4)
        sent_to = now_as_timestamp_protobuf()
        validity_period = ValidityPeriod(sent_from=sent_from, sent_to=sent_to)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        validity_period=validity_period,
                                                        )

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback(
                                                     None))

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=15)

    @staticmethod
    def test_header_query_service_when_senders_is_specified_should_return_the_header_for_this_sender_id():
        """
        Testing Query Header Service when the sender endpoint id is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback(
                                                     None))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        senders=[
                                                            TestQueryHeaderService._sender_onboard_response.get_sensor_alternate_id()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    #

    @staticmethod
    def test_header_query_service_for_specific_message_ids_should_return_the_messages_for_this_specific_message_ids():
        """
        Testing Query Header Service when specific message ids are specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        message_for_message_ids = ['fea31c5c-f5c7-4bf9-b8cc-c183c3248ecf', 'b04cf2bd-b7bb-48ce-9a2b-4a2056521c38']
        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._on_query_header_service_callback(
                                                     message_for_message_ids))

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        message_ids=message_for_message_ids,
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_for_incomplete_attributes_should_return_in_an_error():
        """
        Testing Query Header Service when incomplete attributes are passed
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
    def test_header_query_service_for_incorrect_message_ids_should_return_empty_message():
        """
        Testing Query Header Service when incorrect message ids are specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._incomplete_attributes_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        message_ids=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_for_incorrect_sender_id_should_return_empty_message():
        """
        Testing Query Header Service when incorrect sender id is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._incorrect_ids_callback)

        query_header_parameters = QueryHeaderParameters(application_message_id=new_uuid(),
                                                        application_message_seq_no=current_sequence_number,
                                                        onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                        senders=[new_uuid()],
                                                        )

        query_header_service = QueryHeaderService(messaging_service)
        query_header_service.send(query_header_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def test_header_query_service_for_incorrect_validity_period_should_return_empty_message():
        """
        Testing Query Header Service when incorrect validity period is specified
        """
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                                                 on_message_callback=TestQueryHeaderService._incorrect_ids_callback)

        sent_from = protobuf_timestamp_before_few_seconds(5)
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
    def _feed_delete_service(details, onboard_response, messaging_service):
        """
        Feed Delete Service function to delete messages of specific ids
        """
        TestQueryHeaderService._message_ids_to_clean_up = [header.message_id for header in
                                                           list(details.feed[0].headers)]

        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestQueryHeaderService._recipient_onboard_response.get_sensor_alternate_id())
        delete_message_parameters = FeedDeleteParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number)

        delete_message_parameters.set_message_ids(TestQueryHeaderService._message_ids_to_clean_up)
        delete_message_service = FeedDeleteService(messaging_service)
        delete_message_service.send(delete_message_parameters)

        Sleeper.let_agrirouter_process_the_message(seconds=15)

    @staticmethod
    def _on_query_header_service_callback(message_ids: Optional[list]):
        def _inner_function(client, userdata, msg):
            """
            Callback to decode Query Header Service response
            """
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            while not decoded_message:
                Sleeper.let_agrirouter_process_the_message(seconds=5)

            details = decode_details(decoded_message.response_payload.details)
            details_message_ids = [details.feed[0].headers[idx].message_id for idx in
                                   range(len(details.feed[0].headers))]

            if message_ids:
                assert sorted(details_message_ids) == sorted(message_ids)

            assert decoded_message.response_envelope.type == 6
            assert details.feed[0].headers[0].technical_message_type == CapabilityType.IMG_PNG.value

            if details.query_metrics.total_messages_in_query > 0:
                messaging_service = MqttMessagingService(
                    onboarding_response=TestQueryHeaderService._recipient_onboard_response,
                    on_message_callback=TestQueryHeaderService._on_feed_delete_service_callback)
                TestQueryHeaderService._feed_delete_service(details=details,
                                                            onboard_response=TestQueryHeaderService._recipient_onboard_response,
                                                            messaging_service=messaging_service)

        return _inner_function

    @staticmethod
    def _on_feed_delete_service_callback(client, userdata, msg):
        """
        Callback to decode Feed Delete Service
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message(seconds=5)

        delete_details = decode_details(decoded_message.response_payload.details)
        deleted_message_ids = [idx.args['messageId'] for idx in delete_details.messages]
        assert sorted(TestQueryHeaderService._message_ids_to_clean_up) == sorted(deleted_message_ids)

    @staticmethod
    def _incorrect_ids_callback(client, userdata, msg):
        """
        Callback to decode Query Header Service response when incorrect ids are passed as arguments
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message(seconds=5)

        assert decoded_message.response_envelope.response_code == 204

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

    @staticmethod
    def _incomplete_attributes_callback(client, userdata, msg):
        """
        Callback to decode Query Header Service response when the attributes are incomplete
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
        assert details.messages[
                   0].message == "Query does not contain any filtering criteria: messageIds, senders or validityPeriod. Information required to process message is missing or malformed."
