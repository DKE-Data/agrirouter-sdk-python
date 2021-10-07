from generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from generated.messaging.request.payload.feed.feed_requests_pb2 import MessageConfirm, MessageQuery
from generated.messaging.request.request_pb2 import RequestEnvelope
from messaging.encode import encode_message
from messaging.enums import TechnicalMessageType
from messaging.messages import EncodedMessage
from messaging.parameters.dto import MessageParameters, MessagingParameters
from messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters, CapabilityParameters, \
    FeedConfirmParameters, FeedDeleteParameters, ListEndpointsParameters, SubscriptionParameters, QueryHeaderParameters, \
    QueryMessageParameters
from utils.type_url import TypeUrl
from utils.uuid_util import new_uuid


class AbstractService:

    def __init__(self, messaging_service):
        self.messaging_service = messaging_service

    def send(self, parameters):
        messaging_parameters = MessagingParameters(
            onboarding_response=parameters.get_onboarding_response(),
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
        )
        encoded_messages = self.encode(parameters)
        messaging_parameters.set_encoded_messages([encoded_messages.get_content()])
        return self.messaging_service.send(messaging_parameters)

    @staticmethod
    def encode(*args, **kwargs) -> EncodedMessage:
        ...


class CapabilityService(AbstractService):

    @staticmethod
    def encode(parameters: CapabilityParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.CAPABILITIES.value
        )

        capability_specification = CapabilitySpecification(
            app_certification_id=parameters.get_application_id(),
            app_certification_version_id=parameters.get_certification_version_id(),
            enable_push_notifications=parameters.get_enable_push_notification()
        )
        if parameters.get_capability_parameters():
            capability_specification.capabilities = parameters.get_capability_parameters()

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(CapabilitySpecification.__name__),
            value=capability_specification.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class FeedConfirmService(AbstractService):

    @staticmethod
    def encode(parameters: FeedConfirmParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.FEED_CONFIRM.value
        )

        message_confirm = MessageConfirm(
            message_ids=parameters.get_message_ids()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(MessageConfirm.__name__),
            value=message_confirm.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class FeedDeleteService(AbstractService):

    @staticmethod
    def encode(parameters: FeedDeleteParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.FEED_CONFIRM.value
        )

        message_confirm = MessageConfirm(
            message_ids=parameters.get_message_ids()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(MessageConfirm.__name__),
            value=message_confirm.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class ListEndpointsService(AbstractService):

    @staticmethod
    def encode(parameters: ListEndpointsParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.LIST_ENDPOINTS.value if parameters.is_filtered()
            else TechnicalMessageType.LIST_ENDPOINTS_UNFILTERED.value
        )

        list_endpoints_query = ListEndpointsQuery(
            technical_message_type=parameters.get_technical_message_type(),
            direction=parameters.get_direction()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(ListEndpointsQuery.__name__),
            value=list_endpoints_query.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class QueryMessagesService(AbstractService):

    @staticmethod
    def encode(parameters: QueryMessageParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.FEED_MESSAGE_QUERY.value
        )

        message_query = MessageQuery(
            senders=parameters.get_senders(),
            message_ids=parameters.get_message_ids(),
            validity_period=parameters.get_validity_period(),
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(MessageQuery.__name__),
            value=message_query.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class QueryHeaderService(AbstractService):

    @staticmethod
    def encode(parameters: QueryHeaderParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.FEED_HEADER_QUERY.value
        )

        message_query = MessageQuery(
            senders=parameters.get_senders(),
            message_ids=parameters.get_message_ids(),
            validity_period=parameters.get_validity_period(),
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(MessageQuery.__name__),
            value=message_query.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class SubscriptionService(AbstractService):

    @staticmethod
    def encode(parameters: SubscriptionParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.SUBSCRIPTION.value
        )

        subscription = Subscription(
            technical_message_types=parameters.get_subscription_items(),
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(Subscription.__name__),
            value=subscription.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message