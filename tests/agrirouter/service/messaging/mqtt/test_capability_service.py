import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityDirectionType
from agrirouter.api.enums import CapabilityType
from agrirouter.api.messages import OutboxMessage
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.message_sending import CapabilitiesService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import CapabilitiesParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.applications import CommunicationUnit
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestMqttCapabilitiesService(unittest.TestCase):
    _onboard_response = None
    _messaging_service = None
    _log = logging.getLogger(__name__)
    _callback_processed = False

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                       on_message_callback=self._message_callback)

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

    def _message_callback(self, client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        self._log.info("Received message after sending capabilities: " + str(msg.payload))
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201
        self._callback_processed = True

    def _send_capabilities(self, onboard_response, direction):
        current_sequence_number = SequenceNumberService.next_seq_nr(
            onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
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
