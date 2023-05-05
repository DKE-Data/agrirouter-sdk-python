import pytest

from agrirouter.environments.environments import QAEnvironment
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.onboarding.enums import CertificateTypes, Gateways
from agrirouter.utils.uuid_util import new_uuid
from tests.common.onboarding import onboard_communication_unit
from tests.data.applications import CommunicationUnit
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.sleeper import Sleeper


class TestCreateMessageSenderAndRecipient:

    @staticmethod
    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_create_message_sender_with_pem():
        sender_onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_MESSAGE_SENDER[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="f1d08095a3",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH], sender_onboard_response)

        TestCreateMessageSenderAndRecipient._enable_capabilities(onboard_response=sender_onboard_response,
                                                                 callback=TestCreateMessageSenderAndRecipient._on_message_callback)

    @staticmethod
    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_create_message_recipient_with_pem():
        recipient_onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="8a9440002c",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH],
                                               recipient_onboard_response)

        TestCreateMessageSenderAndRecipient._enable_capabilities(onboard_response=recipient_onboard_response,
                                                                 callback=TestCreateMessageSenderAndRecipient._on_message_callback)

    @staticmethod
    def _enable_capabilities(onboard_response, callback):
        """
        Method to enable capabilities via mqtt
        """
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=callback)
        current_sequence_number = SequenceNumberService.sequence_number_for_endpoint(
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

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_BMP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.let_agrirouter_process_the_message()

    @staticmethod
    def _on_message_callback(msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message()
        assert decoded_message.response_envelope.response_code == 201
