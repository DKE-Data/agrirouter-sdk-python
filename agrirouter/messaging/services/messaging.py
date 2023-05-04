from agrirouter.generated.messaging.request.payload.account.endpoints_pb2 import ListEndpointsQuery
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import MessageConfirm, MessageDelete, \
    MessageQuery
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.encode import encode_message, encode_chunks_message
from agrirouter.messaging.enums import TechnicalMessageType
from agrirouter.messaging.messages import EncodedMessage
from agrirouter.messaging.parameters.dto import MessagingParameters, SendMessageParameters, ChunkedMessageParameters
from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters, \
    CapabilitiesParameters, FeedConfirmParameters, FeedDeleteParameters, ListEndpointsParameters, \
    SubscriptionParameters, QueryHeaderParameters, QueryMessageParameters
from agrirouter.utils.type_url import TypeUrl
from agrirouter.utils.uuid_util import new_uuid


class AbstractService:
    """
    Abstract service class for all services.
    """

    def __init__(self, messaging_service):
        self.messaging_service = messaging_service

    def send(self, parameters):
        """
        Send a message to the agrirouter.
        :param parameters: Parameters for the message.
        """
        messaging_parameters = MessagingParameters(
            onboarding_response=parameters.get_onboarding_response(),
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
        )
        encoded_messages = self.encode(parameters)
        if type(encoded_messages.get_content()) == list:
            messaging_parameters.set_encoded_messages(encoded_messages.get_content())
        else:
            messaging_parameters.set_encoded_messages([encoded_messages.get_content()])

        return self.messaging_service.send(messaging_parameters)

    @staticmethod
    def encode(*args, **kwargs) -> EncodedMessage:
        ...


class CapabilitiesService(AbstractService):
    """
    Service for sending capabilities to the agrirouter.
    """

    @staticmethod
    def encode(parameters: CapabilitiesParameters) -> EncodedMessage:
        """
        Encode the parameters to a message.
        :param parameters: Parameters for the message.
        """
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
            capability_specification.capabilities.extend(parameters.get_capability_parameters())

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(CapabilitySpecification),
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
            type_url=TypeUrl.get_type_url(MessageConfirm),
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
            technical_message_type=TechnicalMessageType.FEED_DELETE.value
        )

        message_delete = MessageDelete(
            message_ids=parameters.get_message_ids(),
            senders=parameters.get_senders(),
            validity_period=parameters.get_validity_period()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(MessageDelete),
            value=message_delete.SerializeToString()
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
            type_url=TypeUrl.get_type_url(ListEndpointsQuery),
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
            type_url=TypeUrl.get_type_url(MessageQuery),
            value=message_query.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class QueryHeaderService(AbstractService):
    """
    Service to receive the headers of the messages
    """

    @staticmethod
    def encode(parameters: QueryHeaderParameters) -> EncodedMessage:
        """
        Encode the parameters into a message
        parameters: QueryHeaderParameters for the service
        """
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
            type_url=TypeUrl.get_type_url(MessageQuery),
            value=message_query.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class SubscriptionService(AbstractService):
    """
    Service for sending subscription messages to the agrirouter.
    """

    @staticmethod
    def encode(parameters: SubscriptionParameters) -> EncodedMessage:
        """
        Encode the parameters into a subscription message.
        parameters: Parameters for the subscription message.
        """
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
            type_url=TypeUrl.get_type_url(Subscription),
            value=subscription.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class SendMessageService(AbstractService):
    """
    Service for sending messages to the agrirouter
    """

    @staticmethod
    def encode(parameters: SendMessageParameters) -> EncodedMessage:
        """
        Encode the parameters into a message.
        parameters: Parameters for the message service.
        """
        message_header_parameters = MessageHeaderParameters(
            technical_message_type=parameters.get_technical_message_type(),
            mode=parameters.get_mode(),
            team_set_context_id=parameters.get_team_set_context_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            recipients=parameters.get_recipients(),
            chunk_component=parameters.get_chunk_components(),
            application_message_id=parameters.get_application_message_id()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=parameters.get_type_url() or TechnicalMessageType.EMPTY.value,
            value=parameters.get_base64_message_content(),
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)

        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class SendChunkedMessageService(AbstractService):
    """
    Service for sending chunked messages to the agrirouter
    """

    @staticmethod
    def encode(parameters: ChunkedMessageParameters):
        """
        parameters: Chunked Message Parameters required
        """
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=parameters.get_encoded_chunked_messages(),
        )
        return encoded_message

