from agrirouter import CapabilitiesService, ListEndpointsService, FeedDeleteService, QueryHeaderService
from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters, \
    CapabilitiesParameters, FeedConfirmParameters, FeedDeleteParameters, ListEndpointsParameters, \
    SubscriptionParameters, QueryHeaderParameters, QueryMessageParameters
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.generated.messaging.response.response_pb2 import ResponseEnvelope
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse
from agrirouter.generated.messaging.response.payload.feed.push_notification_pb2 import PushNotification
from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.enums import CapabilityType, TechnicalMessageType
from agrirouter.messaging.encode import encode_message
from agrirouter.messaging.messages import OutboxMessage, EncodedMessage
from agrirouter.messaging.services.commons import HttpMessagingService
from agrirouter.messaging.parameters.dto import MessagingParameters
from agrirouter.onboarding.enums import GateWays
from agrirouter.onboarding.enums import CertificateTypes
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.uuid_util import new_uuid
from google.protobuf.timestamp_pb2 import Timestamp

from tests import sleeper
from tests.data import applications
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService


class TestSendDirectMessageService:
    sender = OnboardResponseIntegrationService.read("sender")

    def set_capabilities_for_sender(self):
        capabilities_service = CapabilitiesService(messaging_service=HttpMessagingService())
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=self.sender,
            application_id=applications.CommunicationUnit.application_id,
            certification_version_id=applications.CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.value("DISABLED"),
            capability_parameters=[
                CapabilitySpecification.Capability(
                    technical_message_type=CapabilityType.IMG_PNG.value,
                    direction=CapabilitySpecification.Direction.value("SEND_RECEIVE")
                )
            ]
        )
        capabilities_service.send(capabilities_parameters)

        sleeper.let_agrirouter_process_the_message()


