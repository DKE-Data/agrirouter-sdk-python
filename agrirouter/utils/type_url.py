from agrirouter.generated.cloud_provider_integration.cloud_virtualized_app_registration_pb2 import OnboardingResponse, \
    OnboardingRequest
from agrirouter.generated.commons.message_pb2 import Messages
from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import MessageDelete, MessageConfirm, \
    MessageQuery
from agrirouter.generated.messaging.response.payload.account.endpoints_pb2 import ListEndpointsResponse
from agrirouter.generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse, \
    MessageQueryResponse
from agrirouter.messaging.exceptions import TypeUrlNotFoundError


class TypeUrl:
    prefix = "types.agrirouter.com/"

    @classmethod
    def get_type_url(cls, class_):
        if class_ == Messages:
            return cls.prefix + Messages.DESCRIPTOR.full_name
        elif class_ == ListEndpointsResponse:
            return cls.prefix + ListEndpointsResponse.DESCRIPTOR.full_name
        elif class_ == HeaderQueryResponse:
            return cls.prefix + HeaderQueryResponse.DESCRIPTOR.full_name
        elif class_ == MessageQueryResponse:
            return cls.prefix + MessageQueryResponse.DESCRIPTOR.full_name
        elif class_ == MessageDelete:
            return cls.prefix + MessageDelete.DESCRIPTOR.full_name
        elif class_ == MessageConfirm:
            return cls.prefix + MessageConfirm.DESCRIPTOR.full_name
        elif class_ == OnboardingResponse:
            return cls.prefix + OnboardingResponse.DESCRIPTOR.full_name
        elif class_ == OnboardingRequest:
            return cls.prefix + OnboardingRequest.DESCRIPTOR.full_name
        elif class_ == CapabilitySpecification:
            return cls.prefix + CapabilitySpecification.DESCRIPTOR.full_name
        elif class_ == Subscription:
            return cls.prefix + Subscription.DESCRIPTOR.full_name
        elif class_ == MessageQuery:
            return cls.prefix + MessageQuery.DESCRIPTOR.full_name
        elif class_ == ListEndpointsQuery:
            return cls.prefix + ListEndpointsQuery.DESCRIPTOR.full_name
        else:
            raise TypeUrlNotFoundError(f"The {class_} type url not found")
