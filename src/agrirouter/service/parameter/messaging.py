from copy import deepcopy
from typing import List

from agrirouter.api.messages import EncodedMessage
from agrirouter.generated.commons.chunk_pb2 import ChunkComponent
from agrirouter.generated.commons.message_pb2 import Metadata
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from agrirouter.generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from agrirouter.service.dto.response.messaging import BaseOnboardingResponse


class Parameters:
    def __init__(self,
                 *,
                 application_message_seq_no: int,
                 application_message_id: str = None,
                 team_set_context_id: str
                 ):
        self.application_message_seq_no = application_message_seq_no
        self.application_message_id = application_message_id
        self.team_set_context_id = team_set_context_id

    def get_application_message_seq_no(self):
        return self.application_message_seq_no

    def get_application_message_id(self):
        return self.application_message_id

    def get_team_set_context_id(self):
        return self.team_set_context_id

    def set_application_message_seq_no(self, application_message_seq_no):
        self.application_message_seq_no = application_message_seq_no

    def set_application_message_id(self, application_message_id):
        self.application_message_id = application_message_id

    def set_team_set_context_id(self, team_set_context_id):
        self.team_set_context_id = team_set_context_id

    def validate(self):
        pass


class MessageParameters(Parameters):
    def __init__(self,
                 *,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        super(MessageParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
        )

        self.onboarding_response = onboarding_response

    def get_onboarding_response(self) -> BaseOnboardingResponse:
        return self.onboarding_response


class MessagingParameters(MessageParameters):

    def __init__(self,
                 *,
                 application_message_seq_no: int = None,
                 application_message_id: str = None,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 encoded_messages=None
                 ):
        super(MessagingParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response,
        )

        self._encoded_messages = encoded_messages if encoded_messages else []

    def get_encoded_messages(self):
        return deepcopy(self._encoded_messages)

    def set_encoded_messages(self, encoded_messages: List[EncodedMessage]):
        self._encoded_messages = encoded_messages

    def append_encoded_messages(self, encoded_message: EncodedMessage):
        self._encoded_messages.append(encoded_message)

    def extend_encoded_messages(self, encoded_messages: List[EncodedMessage]):
        self._encoded_messages.extend(encoded_messages)


class SendMessageParameters(MessageParameters):
    """
        Parameters to send messages to the agrirouter
        The class inherits from MessageParameters class
    """

    def __init__(self,
                 *,
                 onboarding_response: BaseOnboardingResponse,
                 technical_message_type: str,
                 recipients: list = None,
                 chunk_component=None,
                 base64_message_content: bytes,
                 type_url: str = None,
                 chunk_size: int = None,
                 application_message_id: str,
                 application_message_seq_no: int,
                 mode
                 ):
        """
        onboarding_response: Onboarding response of the sender
        technical_message_type: TechnicalMessageType class to be sent
        recipients: List of recipients
        chunk_components: Chunk Information
        base64_message_content: Message content that is sent
        type_url: Url needed for MessagePayloadParameters
        chunk_size: Define the size of the chunks
        application_message_id: The application message ID
        application_message_seq_no: Sequence number while sending the messages
        to the agrirouter with SequenceNumberService
        """

        super(SendMessageParameters, self).__init__(application_message_id=application_message_id,
                                                    application_message_seq_no=application_message_seq_no,
                                                    onboarding_response=onboarding_response)

        self._technical_message_type = technical_message_type
        self._base64_message_content = base64_message_content
        self._type_url = type_url
        self._mode = mode

        if recipients:
            self._recipients = recipients

        if chunk_component:
            self._chunk_component = chunk_component
        else:
            self._chunk_component = None

        if chunk_size:
            self._chunk_size = chunk_size

    def get_technical_message_type(self):
        return self._technical_message_type

    def get_recipients(self) -> list:
        return self._recipients

    def get_chunk_component(self) -> ChunkComponent:
        return self._chunk_component

    def get_base64_message_content(self):
        return self._base64_message_content

    def get_type_url(self) -> str:
        return self._type_url

    def get_chunk_size(self) -> int:
        return self._chunk_size

    def get_mode(self):
        return self._mode


class ChunkedMessageParameters(MessageParameters):
    """
        Parameters to send chunked messages to the agrirouter
        The class inherits from MessageParameters class
    """

    def __init__(self,
                 *,
                 onboarding_response: BaseOnboardingResponse,
                 technical_message_type: str = None,
                 recipients: List = None,
                 application_message_id: str = None,
                 application_message_seq_no: int = None,
                 encoded_chunked_messages: List[str] = None,
                 ):
        """
        onboarding_response: Onboarding response of the sender
        technical_message_type: TechnicalMessageType class to be sent
        recipients: List of recipients
        application_message_id: The application message ID
        application_message_seq_no: Sequence number while sending the messages
        to the agrirouter with SequenceNumberService
        encoded_chunked_messages: List of encoded chunked messages
        """

        super(ChunkedMessageParameters, self).__init__(application_message_id=application_message_id,
                                                       application_message_seq_no=application_message_seq_no,
                                                       onboarding_response=onboarding_response)

        self._technical_message_type = technical_message_type
        self._recipients = recipients
        self._encoded_chunked_messages = encoded_chunked_messages

    def get_technical_message_type(self):
        return self._technical_message_type

    def set_technical_message_type(self, technical_message_type: str):
        self._technical_message_type = technical_message_type

    def get_recipients(self) -> list:
        return self._recipients

    def set_recipients(self, recipients: list):
        self._recipients = recipients

    def get_encoded_chunked_messages(self) -> List[str]:
        return self._encoded_chunked_messages

    def set_encoded_chunked_messages(self, encoded_chunked_messages: List[str]):
        self._encoded_chunked_messages = encoded_chunked_messages


class MessageHeaderParameters(Parameters):

    def __init__(self,
                 *,
                 technical_message_type: str = None,
                 mode: str = None,
                 team_set_context_id: str = None,
                 application_message_seq_no: int = None,
                 recipients: list = None,
                 chunk_component: ChunkComponent = None,
                 application_message_id: str = None,
                 metadata: Metadata = None
                 ):
        super(MessageHeaderParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id
        )

        self.technical_message_type = technical_message_type
        self.mode = mode
        self.recipients = recipients
        self.chunk_component = chunk_component
        self.metadata = metadata

    def get_technical_message_type(self) -> str:
        return self.technical_message_type

    def get_mode(self) -> str:
        return self.mode

    def get_recipients(self) -> list:
        return self.recipients

    def get_chunk_component(self) -> ChunkComponent:
        return self.chunk_component

    def get_metadata(self) -> Metadata:
        return self.metadata


class MessagePayloadParameters:

    def __init__(self,
                 *,
                 type_url: str,
                 value: str,
                 ):
        self.type_url = type_url
        self.value = value

    def get_type_url(self) -> str:
        return self.type_url

    def get_value(self) -> str:
        return self.value


class CloudOnboardParameters(MessageParameters):

    def __init__(self,
                 *,
                 onboarding_requests: list = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.onboarding_requests = onboarding_requests if onboarding_requests else []
        super(CloudOnboardParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_onboarding_requests(self) -> list:
        return self.onboarding_requests

    def set_onboarding_requests(self, onboarding_requests: list) -> None:
        self.onboarding_requests = onboarding_requests

    def add_onboarding_requests(self, onboarding_request) -> None:
        self.onboarding_requests.append(onboarding_request)

    def extend_onboarding_requests(self, onboarding_requests: list) -> None:
        self.onboarding_requests.extend(onboarding_requests)


class CloudOffboardParameters(MessageParameters):

    def __init__(self,
                 *,
                 endpoints: List[str] = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.endpoints = endpoints if endpoints else []
        super(CloudOffboardParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_endpoints(self) -> List[str]:
        return self.endpoints

    def set_endpoints(self, endpoints: list) -> None:
        self.endpoints = endpoints

    def add_endpoints(self, endpoint: str) -> None:
        self.endpoints.append(endpoint)

    def extend_endpoints(self, endpoints: List[str]) -> None:
        self.endpoints.extend(endpoints)


class CapabilitiesParameters(MessageParameters):

    def __init__(self,
                 *,
                 application_id: str,
                 certification_version_id: str,
                 enable_push_notification: int = CapabilitySpecification.PushNotification.Value("DISABLED"),
                 capability_parameters: List[CapabilitySpecification.Capability] = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.application_id = application_id
        self.certification_version_id = certification_version_id
        self.enable_push_notification = enable_push_notification
        self.capability_parameters = capability_parameters if capability_parameters else []
        super(CapabilitiesParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_application_id(self):
        return self.application_id

    def get_certification_version_id(self):
        return self.certification_version_id

    def get_enable_push_notification(self):
        return self.enable_push_notification

    def get_capability_parameters(self):
        return deepcopy(self.capability_parameters)

    def set_application_id(self, application_id):
        self.application_id = application_id

    def set_certification_version_id(self, certification_version_id):
        self.certification_version_id = certification_version_id

    def set_enable_push_notification(self, enable_push_notification):
        self.enable_push_notification = enable_push_notification

    def set_capability_parameters(self, capability_parameters: list):
        self.capability_parameters = capability_parameters

    def add_capability_parameters(self, capability_parameter):
        self.capability_parameters.append(capability_parameter)

    def extend_capability_parameters(self, capability_parameters: list):
        self.capability_parameters.extend(capability_parameters)


class FeedConfirmParameters(MessageParameters):
    def __init__(self,
                 *,
                 message_ids: list = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.message_ids = message_ids if message_ids else []
        super(FeedConfirmParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_message_ids(self):
        return deepcopy(self.message_ids)

    def set_message_ids(self, message_ids: list):
        self.message_ids = message_ids

    def add_message_ids(self, message_id):
        self.message_ids.append(message_id)

    def extend_message_ids(self, message_ids):
        self.message_ids.extend(message_ids)


class FeedDeleteParameters(MessageParameters):
    def __init__(self,
                 *,
                 message_ids: list = None,
                 senders: list = None,
                 validity_period: ValidityPeriod = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 ):
        self.message_ids = message_ids if message_ids else []
        self.senders = senders if senders else []
        self.validity_period = validity_period
        super(FeedDeleteParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_message_ids(self):
        return deepcopy(self.message_ids)

    def set_message_ids(self, message_ids: list):
        self.message_ids = message_ids

    def add_message_ids(self, message_id):
        self.message_ids.append(message_id)

    def extend_message_ids(self, message_ids):
        self.message_ids.extend(message_ids)

    def get_senders(self):
        return deepcopy(self.senders)

    def set_senders(self, senders: list):
        self.senders = senders

    def add_senders(self, receiver):
        self.senders.append(receiver)

    def extend_senders(self, senders):
        self.senders.extend(senders)

    def get_validity_period(self):
        return self.validity_period

    def set_validity_period(self, validity_period: ValidityPeriod):
        self.validity_period = validity_period


class ListEndpointsParameters(MessageParameters):
    def __init__(self,
                 *,
                 technical_message_type: str = None,
                 direction: int = None,
                 filtered: bool = False,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 ):
        self.technical_message_type = technical_message_type
        self.direction = direction
        self.filtered = filtered
        super(ListEndpointsParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_technical_message_type(self) -> str:
        return self.technical_message_type

    def set_technical_message_type(self, technical_message_type: str):
        self.technical_message_type = technical_message_type

    def get_direction(self) -> int:
        return self.direction

    def set_direction(self, direction: int):
        self.direction = direction

    def is_filtered(self):
        return self.filtered

    def set_filtered(self, filtered: bool):
        self.filtered = filtered


class QueryMessageParameters(MessageParameters):
    def __init__(self,
                 *,
                 senders: list = None,
                 message_ids: list = None,
                 validity_period: ValidityPeriod = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 ):
        self.senders = senders
        self.message_ids = message_ids
        self.validity_period = validity_period
        super(QueryMessageParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_senders(self) -> list:
        return self.senders

    def set_senders(self, senders: list) -> None:
        self.senders = senders

    def add_senders(self, sender) -> None:
        self.senders.append(sender)

    def extend_senders(self, senders) -> None:
        self.senders.extend(senders)

    def get_message_ids(self) -> list:
        return self.message_ids

    def set_message_ids(self, message_ids: list) -> None:
        self.message_ids = message_ids

    def add_message_ids(self, message_id) -> None:
        self.message_ids.append(message_id)

    def extend_message_ids(self, message_ids) -> None:
        self.message_ids.extend(message_ids)

    def get_validity_period(self) -> ValidityPeriod:
        return self.validity_period

    def set_validity_period(self, validity_period: list) -> None:
        self.validity_period = validity_period


class QueryHeaderParameters(MessageParameters):
    def __init__(self,
                 *,
                 senders: list = None,
                 message_ids: list = None,
                 validity_period: ValidityPeriod = None,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 ):
        self.senders = senders
        self.message_ids = message_ids
        self.validity_period = validity_period
        super(QueryHeaderParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_senders(self) -> list:
        return self.senders

    def set_senders(self, senders: list) -> None:
        self.senders = senders

    def add_senders(self, sender) -> None:
        self.senders.append(sender)

    def extend_senders(self, senders) -> None:
        self.senders.extend(senders)

    def get_message_ids(self) -> list:
        return self.message_ids

    def set_message_ids(self, message_ids: list) -> None:
        self.message_ids = message_ids

    def add_message_ids(self, message_id) -> None:
        self.message_ids.append(message_id)

    def extend_message_ids(self, message_ids) -> None:
        self.message_ids.extend(message_ids)

    def get_validity_period(self) -> ValidityPeriod:
        return self.validity_period

    def set_validity_period(self, validity_period: list) -> None:
        self.validity_period = validity_period


class SubscriptionParameters(MessageParameters):
    def __init__(self,
                 *,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 subscription_items: List[Subscription.MessageTypeSubscriptionItem] = None,
                 ):
        self.subscription_items = subscription_items if subscription_items else []
        super(SubscriptionParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_subscription_items(self) -> List[Subscription.MessageTypeSubscriptionItem]:
        return self.subscription_items

    def set_subscription_items(self, subscription_items: List[Subscription.MessageTypeSubscriptionItem]) -> None:
        self.subscription_items = subscription_items

    def add_subscription_items(self, subscription_item: Subscription.MessageTypeSubscriptionItem) -> None:
        self.subscription_items.append(subscription_item)

    def extend_direction(self, subscription_items: List[Subscription.MessageTypeSubscriptionItem]) -> None:
        self.subscription_items.extend(subscription_items)


class ImageParameters(MessageParameters):
    def __init__(self,
                 *,
                 image_encoded: bytes,
                 image_filename: str,
                 application_message_seq_no: int,
                 recipients: list,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.image_encoded = image_encoded
        self.image_filename = image_filename
        self.recipients = recipients
        super(ImageParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_image_encoded(self):
        return self.image_encoded

    def get_image_filename(self):
        return self.image_filename

    def get_recipients(self):
        return self.recipients

    def set_image_encoded(self, image_encoded):
        self.image_encoded = image_encoded

    def set_image_filename(self, image_filename):
        self.image_filename = image_filename

    def set_recipients(self, recipients):
        self.recipients = recipients


class TaskParameters(MessageParameters):
    def __init__(self,
                 *,
                 task_encoded: bytes,
                 task_filename: str,
                 chunk_context_id: str,
                 chunk_current: int,
                 chunk_total: int,
                 chunk_total_size: int,
                 application_message_seq_no: int,
                 recipients: list,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.task_encoded = task_encoded
        self.task_filename = task_filename
        self.recipients = recipients
        self.chunk_context_id = chunk_context_id
        self.chunk_current = chunk_current
        self.chunk_total = chunk_total
        self.chunk_total_size = chunk_total_size
        super(TaskParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_task_encoded(self):
        return self.task_encoded

    def get_task_filename(self):
        return self.task_filename

    def get_chunk_context_id(self):
        return self.chunk_context_id

    def get_chunk_current(self):
        return self.chunk_current

    def get_chunk_total(self):
        return self.chunk_total

    def get_chunk_total_size(self):
        return self.chunk_total_size

    def get_recipients(self):
        return self.recipients

    def set_task_encoded(self, task_encoded):
        self.task_encoded = task_encoded

    def set_task_filename(self, task_filename):
        self.task_filename = task_filename

    def set_chunk_context_id(self, chunk_context_id):
        self.chunk_context_id = chunk_context_id

    def set_chunk_current(self, chunk_current):
        self.chunk_current = chunk_current

    def set_chunk_total(self, chunk_total):
        self.chunk_total = chunk_total

    def set_chunk_total_size(self, chunk_total_size):
        self.chunk_total_size = chunk_total_size

    def set_recipients(self, recipients):
        self.recipients = recipients


class EfdiParameters(MessageParameters):
    def __init__(self,
                 *,
                 efdi: str,
                 efdi_filename: str = None,
                 application_message_seq_no: int,
                 recipients: list = None,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        self.recipients = recipients
        self.efdi = efdi
        self.efdi_filename = efdi_filename
        super(EfdiParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response
        )

    def get_efdi(self):
        return self.efdi

    def get_recipients(self):
        return self.recipients

    def get_efdi_filename(self):
        return self.efdi_filename

    def set_efdi(self, efdi):
        self.efdi = efdi

    def set_recipients(self, recipients):
        self.recipients = recipients

    def set_efdi_filename(self, efdi_filename):
        self.efdi_filename = efdi_filename
