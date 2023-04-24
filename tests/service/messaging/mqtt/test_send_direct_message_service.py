import pytest
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.enums import CapabilityDirectionType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService, SendMessageService, SendMessageParameters
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from tests.sleeper import Sleeper
from tests.data_provider import DataProvider
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope


class TestSendDirectMessageService:
    """
    Test to send the message to a recipient
    The existing sender and recipient PEM onboard responses are read using OnboardIntegrationService
    """
    _recipient_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
    _sender_onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_SENDER_PEM[Identifier.PATH])

    @staticmethod
    def test_given_valid_message_content_when_sending_message_to_single_recipient_then_the_message_should_be_delivered():
        """
        Test for sending the valid message content to a single recipient after enabling IMG_PNG capability with sender and recipient
        Open Connection between Recipient and agrirouter is required. The setup between the sender and the recipient is done before
        running the test. If
        """
        TestSendDirectMessageService._enable_recipient_capabilities_via_mqtt()

        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestSendDirectMessageService._recipient_onboard_response.get_sensor_alternate_id())

        send_message_parameters = SendMessageParameters(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
            technical_message_type=CapabilityType.IMG_PNG.value,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            recipients=[TestSendDirectMessageService._recipient_onboard_response.get_sensor_alternate_id()],
            base64_message_content=DataProvider.read_base64_encoded_image(),
            mode=RequestEnvelope.Mode.Value("DIRECT"))

        messaging_service = MqttMessagingService(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
            on_message_callback=TestSendDirectMessageService._on_message_callback)

        send_message_service = SendMessageService(messaging_service=messaging_service)
        send_message_service.send(send_message_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

    @staticmethod
    def _on_message_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message(seconds=5)

        assert type(decoded_message.response_payload.details.value) == bytes
        assert decoded_message.response_payload.details.value is not None
        assert decoded_message.response_payload is not None

    @staticmethod
    def _enable_sender_capabilities_via_mqtt():
        """
        Method to enable sender capabilities via mqtt
        """

        messaging_service = MqttMessagingService(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
            on_message_callback=TestSendDirectMessageService._on_message_callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestSendDirectMessageService._sender_onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=TestSendDirectMessageService._sender_onboard_response,
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
    def _enable_recipient_capabilities_via_mqtt():
        """
        Method to enable recipient capabilities via mqtt
        """

        messaging_service = MqttMessagingService(
            onboarding_response=TestSendDirectMessageService._recipient_onboard_response,
            on_message_callback=TestSendDirectMessageService._on_message_callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            TestSendDirectMessageService._recipient_onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=TestSendDirectMessageService._recipient_onboard_response,
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
