import logging
import unittest

import pytest

from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.parameters.service import SubscriptionParameters, CapabilitiesParameters
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.messaging.services.messaging import SubscriptionService, CapabilitiesService
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.messages import OutboxMessage
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType
from tests.sleeper import Sleeper


class TestSubscriptionService(unittest.TestCase):
    _onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
    _log = logging.getLogger(__name__)
    _callback_processed = False

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Before each test
        TestSubscriptionService._log.info("Updating capabilities for the test case to ensure a clean state.")
        messaging_service = MqttMessagingService(onboarding_response=TestSubscriptionService._onboard_response,
                                                 on_message_callback=TestSubscriptionService._send_capabilities_callback)
        current_sequence_number = SequenceNumberService.next_seq_nr(
            TestSubscriptionService._onboard_response.get_sensor_alternate_id())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=TestSubscriptionService._onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.DISABLED,
            capability_parameters=[]
        )
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.let_agrirouter_process_the_message()

    @staticmethod
    def _send_capabilities_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        TestSubscriptionService._log.info(
            "Received message from MQTT broker after sending the capabilities, checking the result.")
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = decode_details(decoded_message.response_payload.details)
            TestSubscriptionService._log.error("Message could not be processed. Response code: " + str(
                decoded_message.response_envelope.response_code))
            TestSubscriptionService._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201

    def test_when_sending_subscriptions_for_pem_recipient_then_the_server_should_accept_them(self):
        """
        Sending subscriptions via mqtt with the existing onboard response and callback as arguments
        """
        self._log.info("Sending subscriptions via mqtt with the existing onboard response and callback as arguments.")
        messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                 on_message_callback=TestSubscriptionService._send_subscription_callback)
        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._onboard_response.get_sensor_alternate_id())
        subscription_service = SubscriptionService(messaging_service)
        technical_msg_type = CapabilityType.ISO_11783_TASK_DATA_ZIP.value
        subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=technical_msg_type)
        subscription_parameters = SubscriptionParameters(
            subscription_items=[subscription_item],
            onboarding_response=self._onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
        )
        subscription_service.send(subscription_parameters)
        Sleeper.let_agrirouter_process_the_message()

        if not self._callback_processed:
            self._log.error("There was no answer from the agrirouter, the test will fail.")

        self.assertTrue(self._callback_processed)
        self._callback_processed = False

    @staticmethod
    def _send_subscription_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        TestSubscriptionService._log.info(
            "Received message from MQTT broker after sending the subscriptions, checking the result.")
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        if decoded_message.response_envelope.response_code != 201:
            decoded_details = decode_details(decoded_message.response_payload.details)
            TestSubscriptionService._log.error("Message could not be processed. Response code: " + str(
                decoded_message.response_envelope.response_code))
            TestSubscriptionService._log.error("Message details: " + str(decoded_details))
        assert decoded_message.response_envelope.response_code == 201
        TestSubscriptionService._callback_processed = True
