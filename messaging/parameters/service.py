from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

from generated.commons.chunk_pb2 import ChunkComponent
from generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription
from generated.messaging.request.payload.feed.feed_requests_pb2 import ValidityPeriod
from messaging.parameters.dto import MessageParameters, Parameters


class MessageHeaderParameters(Parameters):

    def __init__(self,
                 *,
                 technical_message_type: str = None,
                 mode: str = None,
                 team_set_context_id: str = None,
                 application_message_seq_no: str = None,
                 recipients: list = None,
                 chunk_component: ChunkComponent = None,
                 application_message_id: int = None,
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

    def get_technical_message_type(self) -> str:
        return self.technical_message_type

    def get_mode(self) -> str:
        return self.mode

    def get_recipients(self) -> list:
        return self.recipients

    def get_chunk_component(self) -> ChunkComponent:
        return self.chunk_component


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


class CapabilityParameters(MessageParameters):

    def __init__(self,
                 application_id,
                 certification_version_id,
                 enable_push_notification,
                 capability_parameters: list = None,
                 **kwargs
                 ):
        self.application_id = application_id
        self.certification_version_id = certification_version_id
        self.enable_push_notification = enable_push_notification
        self.capability_parameters = capability_parameters if capability_parameters else []
        super(CapabilityParameters, self).__init__(**kwargs)

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
    def __init__(self, message_ids: list = None, **kwargs):
        self.message_ids = message_ids if message_ids else []
        super(FeedConfirmParameters, self).__init__(**kwargs)

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
                 message_ids: list = None,
                 receivers: list = None,
                 validity_period: ValidityPeriod = None,
                 **kwargs):
        self.message_ids = message_ids if message_ids else []
        self.receivers = receivers if receivers else []
        self.validity_period = validity_period
        super(FeedDeleteParameters, self).__init__(**kwargs)

    def get_message_ids(self):
        return deepcopy(self.message_ids)

    def set_message_ids(self, message_ids: list):
        self.message_ids = message_ids

    def add_message_ids(self, message_id):
        self.message_ids.append(message_id)

    def extend_message_ids(self, message_ids):
        self.message_ids.extend(message_ids)

    def get_receivers(self):
        return deepcopy(self.receivers)

    def set_receivers(self, receivers: list):
        self.receivers = receivers

    def add_receivers(self, receiver):
        self.receivers.append(receiver)

    def extend_receivers(self, receivers):
        self.receivers.extend(receivers)

    def get_validity_period(self):
        return self.validity_period

    def set_validity_period(self, validity_period: ValidityPeriod):
        self.validity_period = validity_period


class ListEndpointsParameters(MessageParameters):
    def __init__(self,
                 technical_message_type: str = None,
                 direction: str = None,
                 filtered: bool = False,
                 **kwargs):
        self.technical_message_type = technical_message_type
        self.direction = direction
        self.filtered = filtered
        super(ListEndpointsParameters, self).__init__(**kwargs)

    def get_technical_message_type(self) -> str:
        return self.technical_message_type

    def set_technical_message_type(self, technical_message_type: str):
        self.technical_message_type = technical_message_type

    def get_direction(self) -> str:
        return self.direction

    def set_direction(self, direction: str):
        self.direction = direction

    def is_filtered(self):
        return self.filtered

    def set_filtered(self, filtered: bool):
        self.filtered = filtered


class SubscriptionParameters(MessageParameters):
    def __init__(self,
                 subscription_items: List[Subscription.MessageTypeSubscriptionItem] = None,
                 **kwargs):
        self.subscription_items = subscription_items if subscription_items else []
        super(SubscriptionParameters, self).__init__(**kwargs)

    def get_subscription_items(self) -> List[Subscription.MessageTypeSubscriptionItem]:
        return self.subscription_items

    def set_subscription_items(self, subscription_items: List[Subscription.MessageTypeSubscriptionItem]) -> None:
        self.subscription_items = subscription_items

    def add_subscription_items(self, subscription_item: Subscription.MessageTypeSubscriptionItem) -> None:
        self.subscription_items.append(subscription_item)

    def extend_direction(self, subscription_items: List[Subscription.MessageTypeSubscriptionItem]) -> None:
        self.subscription_items.extend(subscription_items)
