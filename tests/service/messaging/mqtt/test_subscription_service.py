import pytest
from agrirouter.messaging.parameters.service import SubscriptionParameters
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.messaging.services.messaging import SubscriptionService
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.messages import OutboxMessage
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from agrirouter.messaging.enums import CapabilityType
from tests.sleeper import Sleeper


class TestMqttSubscriptionService:

    def test_when_sending_subscriptions_for_pem_recipient_then_the_server_should_accept_them(self):
        """
        Load the existing onboard response and send the subscriptions via mqtt
        """
        _onboard_response = OnboardResponseIntegrationService.read(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH])
        TestMqttSubscriptionService._send_subscriptions_via_mqtt(onboard_response=_onboard_response,
                                                                 mqtt_message_callback=TestMqttSubscriptionService._on_message_callback)

    @staticmethod
    def _on_message_callback(client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = decode_response(outbox_message.command.message.encode())
        while not decoded_message:
            Sleeper.let_agrirouter_process_the_message()
        assert decoded_message.response_envelope.response_code == 201

    @staticmethod
    def _send_subscriptions_via_mqtt(onboard_response, mqtt_message_callback):
        """
        Sending subscriptions via mqtt with the existing onboard response and callback as arguments
        """
        messaging_service = MqttMessagingService(onboarding_response=onboard_response,
                                                 on_message_callback=mqtt_message_callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
            onboard_response.get_sensor_alternate_id())
        subscription_service = SubscriptionService(messaging_service)
        technical_msg_type = CapabilityType.ISO_11783_TASK_DATA_ZIP.value
        subscription_item = Subscription.MessageTypeSubscriptionItem(technical_message_type=technical_msg_type)
        subscription_parameters = SubscriptionParameters(
            subscription_items=[subscription_item],
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=current_sequence_number,
        )
        subscription_service.send(subscription_parameters)
        Sleeper.let_agrirouter_process_the_message()
