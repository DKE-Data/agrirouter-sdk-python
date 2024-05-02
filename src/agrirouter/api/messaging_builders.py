from typing import List

from agrirouter.api.enums import CapabilityType
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.generated.messaging.request.payload.endpoint.subscription_pb2 import Subscription


class SubscriptionItemBuilder:

    def __init__(self):
        self._subscription_items = []

    def build(self):
        return self._subscription_items

    def clear(self):
        self._subscription_items = []

    def with_task_data(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_device_description(self, ddis: List[int] = None, position: bool = None):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.ISO_11783_DEVICE_DESCRIPTION.value,
            ddis=ddis,
            position=position
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_time_log(self, ddis: List[int] = None, position: bool = None):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.ISO_11783_TIMELOG.value,
            ddis=ddis,
            position=position
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_bmp(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.IMG_BMP.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_jpg(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.IMG_JPEG.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_png(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.IMG_PNG.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_shape(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.SHP_SHAPE_ZIP.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_pdf(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.DOC_PDF.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_avi(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.VID_AVI.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_mp4(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.VID_MP4.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_wmv(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.VID_WMV.value
        )
        self._subscription_items.append(subscription_item)
        return self

    def with_gps_info(self):
        subscription_item = Subscription.MessageTypeSubscriptionItem(
            technical_message_type=CapabilityType.GPS_INFO.value
        )
        self._subscription_items.append(subscription_item)
        return self


class CapabilityBuilder:

    def __init__(self):
        self._capabilities = []

    def build(self) -> list:
        return self._capabilities

    def clear(self):
        self._capabilities = []

    def with_task_data(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.ISO_11783_TASK_DATA_ZIP.value
        self._capabilities.append(capability)
        return self

    def with_device_description(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.ISO_11783_DEVICE_DESCRIPTION.value
        self._capabilities.append(capability)
        return self

    def with_time_log(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.ISO_11783_TIMELOG.value
        self._capabilities.append(capability)
        return self

    def with_bmp(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.IMG_BMP.value
        self._capabilities.append(capability)
        return self

    def with_jpg(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.IMG_JPEG.value
        self._capabilities.append(capability)
        return self

    def with_png(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.IMG_PNG.value
        self._capabilities.append(capability)
        return self

    def with_shape(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.SHP_SHAPE_ZIP.value
        self._capabilities.append(capability)
        return self

    def with_pdf(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.DOC_PDF.value
        self._capabilities.append(capability)
        return self

    def with_avi(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.VID_AVI.value
        self._capabilities.append(capability)
        return self

    def with_mp4(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.VID_MP4.value
        self._capabilities.append(capability)
        return self

    def with_wmv(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.VID_WMV.value
        self._capabilities.append(capability)
        return self

    def with_gps_info(self, direction: int):
        capability = CapabilitySpecification.Capability()
        capability.direction = direction
        capability.technical_message_type = CapabilityType.GPS_INFO.value
        self._capabilities.append(capability)
        return self
