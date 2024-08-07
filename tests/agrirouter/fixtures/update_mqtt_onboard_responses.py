import pytest

from agrirouter.api.enums import CapabilityType, CapabilityDirectionType
from agrirouter.api.enums import CertificateTypes, Gateways
from agrirouter.api.env import Qa
from agrirouter.api.messages import OutboxMessage
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.message_sending import CapabilitiesService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import CapabilitiesParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.onboarding import onboard_communication_unit
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.applications import CommunicationUnit
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import save_onboard_response


class TestSingleMqttEndpointWithPEMCertificate:

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient_with_pem(self):
        """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_RECIPIENT_PEM[Identifier.ID],
            _environment=Qa(),
            registration_code="e53438a6b3",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )
        save_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH], onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_sender_with_pem(self):
        """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_SENDER_PEM[Identifier.ID],
            _environment=Qa(),
            registration_code="7ac0514114",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )
        save_onboard_response(Identifier.MQTT_SENDER_PEM[Identifier.PATH], onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_messages_sender_with_pem(self):
        sender_onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_MESSAGES_SENDER[Identifier.ID],
            _environment=Qa(),
            registration_code="26b37bc999",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )
        save_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH], sender_onboard_response)
        self._enable_capabilities(onboard_response=sender_onboard_response, callback=self._on_message_callback)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_messages_recipient_with_pem(self):
        recipient_onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.ID],
            _environment=Qa(),
            registration_code="4f4bac3b04",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )
        save_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH],
                              recipient_onboard_response)
        self._enable_capabilities(onboard_response=recipient_onboard_response,
                                  callback=self._on_message_callback)

    @staticmethod
    def _enable_capabilities(onboard_response, callback):
        """
        Method to enable capabilities via mqtt
        """
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=callback)
        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
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

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_DEVICE_DESCRIPTION.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TIMELOG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.process_the_command()

    @staticmethod
    def _on_message_callback(msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.process_the_command()
        assert decoded_message.response_envelope.response_code == 201
