import logging
import unittest

from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.enums import CapabilityDirectionType
from agrirouter.messaging.enums import CapabilityType
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.services.messaging import CapabilitiesService
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from agrirouter.utils.uuid_util import new_uuid
from tests.data.applications import CommunicationUnit
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import read_onboard_response
from tests.sleeper import Sleeper


class TestMqttCapabilitiesService(unittest.TestCase):
    _log = logging.getLogger(__name__)
    _callback_processed = False

    def test_when_sending_capabilities_for_recipient_with_direction_send_receive_then_the_server_should_accept_them(
            self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'SEND_RECEIVE' direction
        """
        _onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._send_capabilities(onboard_response=_onboard_response,
                                mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                direction=CapabilityDirectionType.SEND_RECEIVE.value)

    def test_when_sending_capabilities_for_recipient_with_direction_receive_then_the_server_should_accept_them(self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'RECEIVE' direction
        """
        _onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._send_capabilities(onboard_response=_onboard_response,
                                mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                direction=CapabilityDirectionType.RECEIVE.value)

    def test_when_sending_capabilities_for_recipient_with_direction_send_then_the_server_should_accept_them(self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'SEND' direction
        """
        _onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._send_capabilities(onboard_response=_onboard_response,
                                mqtt_message_callback=TestMqttCapabilitiesService._on_message_callback,
                                direction=CapabilityDirectionType.SEND.value)

    @staticmethod
    def _on_message_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        TestMqttCapabilitiesService._log.info("Received message after sending capabilities: " + str(msg.payload))
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = decode_details(decoded_message.response_payload.details)
        TestMqttCapabilitiesService._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201
        TestMqttCapabilitiesService._callback_processed = True

    def _send_capabilities(self, onboard_response, mqtt_message_callback, direction):
        messaging_service = MqttMessagingService(onboarding_response=onboard_response,
                                                 on_message_callback=mqtt_message_callback)
        current_sequence_number = SequenceNumberService.next_seq_nr(
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
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False
