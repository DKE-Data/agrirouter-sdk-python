import pytest
import time
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.enums import CapabilityDirectionType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier


class TestMqttCapabilitiesService:

    def test_update_recipient_with_direction_send_receive(self):
        """
            Load Onboard Response from 'Mqtt/CommunicationUnit/PEM/Recipient' and test with 'SEND_RECEIVE' direction
        """
        _onboard_response = TestMqttCapabilitiesService.load_onboard_response(
            Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        TestMqttCapabilitiesService._enable_all_capabilities_via_mqtt(onboard_response=_onboard_response,
                                                                      mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                                                      direction=CapabilityDirectionType.SEND_RECEIVE.value)

    def test_update_recipient_with_direction_receive(self):
        """
            Load Onboard Response from 'Mqtt/CommunicationUnit/PEM/Recipient' and test with 'RECEIVE' direction
        """
        _onboard_response = TestMqttCapabilitiesService.load_onboard_response(
            Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        TestMqttCapabilitiesService._enable_all_capabilities_via_mqtt(onboard_response=_onboard_response,
                                                                      mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                                                      direction=CapabilityDirectionType.RECEIVE.value)

    def test_update_recipient_with_direction_send(self):
        """
            Load Onboard Response from 'Mqtt/CommunicationUnit/PEM/Recipient' and test with 'SEND' direction
        """
        _onboard_response = TestMqttCapabilitiesService.load_onboard_response(
            Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        TestMqttCapabilitiesService._enable_all_capabilities_via_mqtt(onboard_response=_onboard_response,
                                                                      mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                                                      direction=CapabilityDirectionType.SEND.value)

    @staticmethod
    def load_onboard_response(path):
        """
        Static method to load the onboard response
        """
        recorded_onboard_response = OnboardResponseIntegrationService.read(path)
        return recorded_onboard_response

    @staticmethod
    def _on_message_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            time.sleep(5)
        assert decoded_message.response_envelope.response_code == 201

    @staticmethod
    def _enable_all_capabilities_via_mqtt(onboard_response, mqtt_message_callback, direction):
        messaging_service = MqttMessagingService(onboarding_response=onboard_response,
                                                 on_message_callback=mqtt_message_callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.DISABLED,
            capability_parameters=[]
        )
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=direction))
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        time.sleep(5)
