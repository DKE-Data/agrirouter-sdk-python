import pytest
import time
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.decode import decode_details
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.data.identifier import Identifier
import logging


class TestMqttCapabilitiesService:

    # @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient(self):
        """
            Load Onboard Response from 'Mqtt/CommunicationUnit/PEM/Recipient'
        """
        self._onboard_response = TestMqttCapabilitiesService.load_onboard_response(r'Mqtt/CommunicationUnit/PEM/Recipient')
        self._response = self._enable_all_capabilities_via_mqtt(self._onboard_response, self._on_message_callback)

    @staticmethod
    def load_onboard_response(path):
        recorded_onboard_response = OnboardResponseIntegrationService.read(path)
        return recorded_onboard_response

    def _on_message_callback(self, client, userdata, msg):
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message)

        while not decoded_message:
            time.sleep(5)

        assert decoded_message.response_envelope.response_code == 201

        try:
            decoded_details = decode_details(decoded_message.response_payload.details)
            logging.info(decoded_details)
        except Exception as exc:
            logging.error(exc)


    def _enable_all_capabilities_via_mqtt(self, onboard_response, mqtt_message_callback):
        messaging_service = MqttMessagingService(onboarding_response=onboard_response,
                                                 on_message_callback=mqtt_message_callback)
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=Identifier.MQTT_RECIPIENT_PEM[Identifier.ID],
            application_message_seq_no=1,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.DISABLED,
            capability_parameters=[]
        )

        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASKDATA_ZIP.value,
                                               direction="SEND_RECEIVE"))
        response = capabilities_service.send(capabilities_parameters)

        return response
