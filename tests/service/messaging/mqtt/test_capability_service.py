import logging
import unittest

import pytest

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
from tests.common.sleeper import Sleeper


class TestMqttCapabilitiesService(unittest.TestCase):
    _onboard_response = None
    _messaging_service = None
    _log = logging.getLogger(__name__)
    _callback_processed = False

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                       on_message_callback=self._message_callback())

        yield

        self._messaging_service.client.disconnect()

    def test_when_sending_capabilities_for_recipient_with_direction_send_receive_then_the_server_should_accept_them(
            self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'SEND_RECEIVE' direction
        """
        self._send_capabilities(onboard_response=self._onboard_response,
                                direction=CapabilityDirectionType.SEND_RECEIVE.value)

    def test_when_sending_capabilities_for_recipient_with_direction_receive_then_the_server_should_accept_them(self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'RECEIVE' direction
        """
        self._send_capabilities(onboard_response=self._onboard_response,
                                direction=CapabilityDirectionType.RECEIVE.value)

    def test_when_sending_capabilities_for_recipient_with_direction_send_then_the_server_should_accept_them(self):
        """
            Load onboard response from 'Mqtt/CommunicationUnit/PEM/Recipient' and send with 'SEND' direction
        """
        self._send_capabilities(onboard_response=self._onboard_response,
                                direction=CapabilityDirectionType.SEND.value)

    def _message_callback(self):
        def _inner_function(client, userdata, msg):
            """
            Callback to handle the incoming messages from the MQTT broker
            """
            self._log.info("Received message after sending capabilities: " + str(msg.payload))
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = decode_response(outbox_message.command.message.encode())
            if decoded_message.response_envelope.response_code != 201:
                decoded_details = decode_details(decoded_message.response_payload.details)
                self._log.error("Message details: " + str(decoded_details))
            assert decoded_message.response_envelope.response_code == 201
            self._callback_processed = True

        return _inner_function

    def _send_capabilities(self, onboard_response, direction):
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
        capabilities_service = CapabilitiesService(self._messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False
