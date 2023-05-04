import pytest
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from tests.sleeper import Sleeper
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType, TechnicalMessageType
from agrirouter.messaging.services.messaging import CapabilitiesService, SendChunkedMessageService
from agrirouter.messaging.parameters.dto import ChunkedMessageParameters
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from tests.data.applications import CommunicationUnit
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from tests.data_provider import DataProvider
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters
from agrirouter.messaging.encode import chunk_and_base64encode_each_chunk, encode_chunks_message


class TestSendAndReceiveChunkedMessages:
    _recipient_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH])
    _chunked_message_to_verify = []
    _MAX_CHUNK_SIZE = 1024000

    @staticmethod
    def test_send_direct_chunked_message():
        """
        Test sending direct chunked messages with the push notifications enabled.
        The setup between recipient and sender, like, enabling capabilities and routing has been done prior to running
        this test
        """

        TestSendAndReceiveChunkedMessages._enable_capabilities_via_mqtt(onboard_response=TestSendAndReceiveChunkedMessages._recipient_onboard_response,
                                                                        callback=TestSendAndReceiveChunkedMessages._on_message_capabilities_callback)


        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestSendAndReceiveChunkedMessages._recipient_onboard_response.get_sensor_alternate_id())

        messaging_service = MqttMessagingService(onboarding_response=TestSendAndReceiveChunkedMessages._sender_onboard_response,
                                                 on_message_callback=TestSendAndReceiveChunkedMessages._on_message_capabilities_callback)

        message_header_parameters = MessageHeaderParameters(application_message_id=new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            technical_message_type=CapabilityType.IMG_BMP.value,
                                                            recipients=[TestSendAndReceiveChunkedMessages._recipient_onboard_response.get_sensor_alternate_id()],
                                                            mode=RequestEnvelope.Mode.Value("DIRECT"))

        message_payload_parameters = MessagePayloadParameters(type_url=TechnicalMessageType.EMPTY.value,
                                                              value=DataProvider.read_base64_encoded_large_bmp())

        message_parameter_tuples = chunk_and_base64encode_each_chunk(header_parameters=message_header_parameters,
                                                                     payload_parameters=message_payload_parameters,
                                                                     onboarding_response=TestSendAndReceiveChunkedMessages._sender_onboard_response)

        for _tuple in message_parameter_tuples:
            TestSendAndReceiveChunkedMessages._chunked_message_to_verify.append(_tuple.message_payload_parameters.get_value())
            assert len(_tuple.message_payload_parameters.get_value()) <= TestSendAndReceiveChunkedMessages._MAX_CHUNK_SIZE

        encoded_chunked_messages = encode_chunks_message(message_parameter_tuple=message_parameter_tuples)

        chunk_message_parameters = ChunkedMessageParameters(
            onboarding_response=TestSendAndReceiveChunkedMessages._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_BMP.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[TestSendAndReceiveChunkedMessages._recipient_onboard_response.get_sensor_alternate_id()],
            encoded_chunked_messages=encoded_chunked_messages)

        send_chunked_message_service = SendChunkedMessageService(messaging_service=messaging_service)
        send_chunked_message_service.send(chunk_message_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=10)


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
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_BMP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_PNG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_JPEG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)

        Sleeper.let_agrirouter_process_the_message(seconds=5)


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
        assert decoded_message.response_envelope.response_code == 200 or 201
        if decoded_message.response_envelope.type == 12:
            push_notification = decode_details(decoded_message.response_payload.details)
            current_chunked_message = push_notification.messages[0].content.value
            assert decoded_message.response_envelope.response_code == 200
            assert DataProvider.get_hash(current_chunked_message) == DataProvider.get_hash(TestSendAndReceiveChunkedMessages._chunked_message_to_verify[0])
            TestSendAndReceiveChunkedMessages._chunked_message_to_verify.pop(0)
