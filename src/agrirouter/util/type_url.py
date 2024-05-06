from agrirouter.api.exceptions import TypeUrlNotFound
from agrirouter.generated.cloud_provider_integration.cloud_virtualized_app_registration_pb2 import \
    OnboardingResponse, \
    OnboardingRequest
from agrirouter.generated.commons.message_pb2 import Messages
from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.generated.messaging.request.payload.efdi.efdi_pb2 import TimeLog, ISO11783_TaskData
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import MessageDelete, MessageConfirm, \
    MessageQuery
from agrirouter.generated.messaging.response.payload.account.endpoints_pb2 import ListEndpointsResponse
from agrirouter.generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse, \
    MessageQueryResponse
from agrirouter.generated.messaging.response.payload.feed.push_notification_pb2 import PushNotification


class TypeUrl:
    prefix = "types.agrirouter.com/"
    commands = (
        Messages,
        ListEndpointsResponse,
        HeaderQueryResponse,
        MessageQueryResponse,
        MessageDelete,
        MessageConfirm,
        OnboardingResponse,
        OnboardingRequest,
        CapabilitySpecification,
        Subscription,
        MessageQuery,
        ListEndpointsQuery,
        PushNotification,
        TimeLog,
        ISO11783_TaskData
    )

    @classmethod
    def get_type_url(cls, class_):
        return TypeUrl.get_command(class_)

    @classmethod
    def get_command(cls, class_) -> str:
        if class_ not in cls.commands:
            raise TypeUrlNotFound(f"The {class_} type url not found")
        return cls.prefix + class_.DESCRIPTOR.full_name
