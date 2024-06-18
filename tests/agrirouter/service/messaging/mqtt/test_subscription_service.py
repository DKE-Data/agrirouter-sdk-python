import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType, CapabilityDirectionType
from agrirouter.api.messages import OutboxMessage
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.message_sending import CapabilitiesService, SubscriptionService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import SubscriptionParameters, CapabilitiesParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.applications import CommunicationUnit
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestSubscriptionService(unittest.TestCase):
    _messaging_service = None
    _onboard_response = None
    _log = logging.getLogger(__name__)
    _callback_processed = False

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Before each test
        self._onboard_response = read_onboard_response(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        self._send_capabilities()
        self._messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                       on_message_callback=self._send_subscription_callback)

    def _send_capabilities(self):
        """
            Send capabilities to the AR with the given messaging service.
        """
        self._log.info("Updating capabilities for the test case to ensure a clean state.")
        messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                 on_message_callback=self._send_capabilities_callback)
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=self._onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.DISABLED,
            capability_parameters=[]
        )
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_PNG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_BMP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_JPEG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.process_the_command()
        self.assertTrue(self._callback_processed)
        self._callback_processed = False
        messaging_service.client.disconnect()

    def _send_capabilities_callback(self, client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        self._log.info(
            "Received message from MQTT broker after sending the capabilities, checking the result.")
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.error("Message could not be processed. Response code: " + str(
                decoded_message.response_envelope.response_code))
            self._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201
        self._callback_processed = True

    def test_when_sending_subscriptions_for_pem_recipient_then_the_server_should_accept_them(self):
        """
        Sending subscriptions via mqtt with the existing onboard response and callback as arguments
        """
        self._log.info("Sending subscriptions via mqtt with the existing onboard response and callback as arguments.")
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._onboard_response.get_sensor_alternate_id())
        subscription_service = SubscriptionService(self._messaging_service)
        technical_msg_type = CapabilityType.IMG_PNG.value
        subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=technical_msg_type)
        subscription_parameters = SubscriptionParameters(
            subscription_items=[subscription_item],
            onboarding_response=self._onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
            application_message_seq_no=current_sequence_number,
        )
        subscription_service.send(subscription_parameters)
        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error(
                "Either the subscription callback was not processed in time or there was an error during the checks.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    def _send_subscription_callback(self, client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        self._log.info(
            "Received message from MQTT broker after sending the subscriptions, checking the result.")
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201
        self._callback_processed = True
