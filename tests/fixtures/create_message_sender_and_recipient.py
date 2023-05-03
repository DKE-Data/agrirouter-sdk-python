import pytest
from agrirouter import QueryHeaderService, QueryHeaderParameters, FeedDeleteService, FeedDeleteParameters, \
    OnboardingService, OnboardParameters
from agrirouter.environments.environments import QAEnvironment
from agrirouter.messaging.decode import decode_response, decode_details
from agrirouter.messaging.messages import OutboxMessage
from agrirouter.messaging.services.commons import MqttMessagingService
from agrirouter.onboarding.enums import CertificateTypes, Gateways
from agrirouter.onboarding.response import OnboardResponse
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from agrirouter.utils.uuid_util import new_uuid
from agrirouter.messaging.services.sequence_number_service import SequenceNumberService
from tests.data.identifier import Identifier
from tests.sleeper import Sleeper
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.utils.utc_time_util import now_as_timestamp_protobuf, protobuf_timestamp_before_number_of_weeks, \
    protobuf_timestamp_before_few_seconds
from agrirouter.messaging.services.messaging import CapabilitiesService, SendMessageService, SendMessageParameters
from agrirouter.messaging.parameters.service import CapabilitiesParameters
from tests.data.applications import CommunicationUnit
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from tests.data_provider import DataProvider
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from typing import Optional


class TestCreateMessageSenderAndRecipient:

    @staticmethod
    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_create_message_sender_with_pem(onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_MESSAGE_SENDER[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="ef0f89246d",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_MESSAGE_SENDER[Identifier.PATH], onboard_response)

    @staticmethod
    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_create_message_recipient_with_pem(onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="ef0f89246d",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_MESSAGE_RECIPIENT[Identifier.PATH], onboard_response)

    @staticmethod
    def onboarding_process_fixture():
        """ Fixture for the onboarding process. """

        def __onboard(uuid: str, _environment, registration_code: str, certification_type_definition: str = "PEM",
                      gateway_id: str = "2") -> OnboardResponse:
            onboarding_service = OnboardingService(env=_environment)
            onboarding_parameters = OnboardParameters(
                id_=uuid,
                reg_code=registration_code,
                certificate_type=certification_type_definition,
                gateway_id=gateway_id,
                application_id=CommunicationUnit.application_id,
                certification_version_id=CommunicationUnit.certification_version_id,
                time_zone="+01:00"
            )

            onboard_response = onboarding_service.onboard(onboarding_parameters)
            assert onboard_response.device_alternate_id != ''
            assert onboard_response.sensor_alternate_id != ''
            assert onboard_response.capability_alternate_id != ''
            assert onboard_response.authentication.certificate != ''
            assert onboard_response.authentication.secret != ''
            assert onboard_response.authentication.type != ''
            assert onboard_response.connection_criteria.commands != ''
            assert onboard_response.connection_criteria.measures != ''

            return onboard_response

        return __onboard

    @staticmethod
    def _enable_capabilities_via_mqtt(onboard_response, callback):
        """
        Method to enable capabilities via mqtt
        """
        messaging_service = MqttMessagingService(
            onboarding_response=onboard_response,
            on_message_callback=callback)
        current_sequence_number = SequenceNumberService.generate_sequence_number_for_endpoint(
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

        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_service.send(capabilities_parameters)
        Sleeper.let_agrirouter_process_the_message(seconds=5)

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
