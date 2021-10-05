from generated.cloud_provider_integration.cloud_virtualized_app_registration_pb2 import OnboardingResponse, \
    OnboardingRequest
from generated.commons.message_pb2 import Messages
from generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from generated.messaging.request.payload.feed.feed_requests_pb2 import MessageDelete, MessageConfirm, MessageQuery
from generated.messaging.response.payload.account.endpoints_pb2 import ListEndpointsResponse
from generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse, MessageQueryResponse
from messaging.exceptions import TypeUrlNotFoundError


class TypeUrl:
    prefix = "types.agrirouter.com/"

    @classmethod
    def get_type_url(cls, class_):
        if class_.__name__ == Messages.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == ListEndpointsResponse.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == HeaderQueryResponse.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == MessageQueryResponse.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == MessageDelete.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == MessageConfirm.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == OnboardingResponse.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == OnboardingRequest.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == CapabilitySpecification.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == Subscription.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == MessageQuery.__name__:
            return cls.prefix + class_.__name__
        elif class_.__name__ == ListEndpointsQuery.__name__:
            return cls.prefix + class_.__name__
        else:
            raise TypeUrlNotFoundError(f"The {class_} type url not found")
