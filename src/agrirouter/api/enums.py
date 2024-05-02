from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values_list(cls):
        return [key.value for key in cls]


class ResponseTypes(BaseEnum):
    VERIFY = "verify"
    ONBOARD = "onboard"


class ContentTypes(BaseEnum):
    APPLICATION_JSON = "application/json"


class Environments(BaseEnum):
    PRODUCTION: str = "production"
    QA: str = "qa"


class RequestHeaders(BaseEnum):
    AUTHORIZATION: str = "Authorization"
    X_AGRIROUTER_SIGNATURE: str = "X-Agrirouter-Signature"
    CONTENT_TYPE: str = "Content-Type"
    X_AGRIROUTER_APPLICATION_ID: str = "X-Agrirouter-ApplicationId"


class TechnicalMessageType(BaseEnum):
    """
    Technical message type.
    """

    EMPTY = ""
    CAPABILITIES = "dke:capabilities"
    SUBSCRIPTION = "dke:subscription"
    LIST_ENDPOINTS = "dke:list_endpoints"
    LIST_ENDPOINTS_UNFILTERED = "dke:list_endpoints_unfiltered"
    FEED_CONFIRM = "dke:feed_confirm"
    FEED_DELETE = "dke:feed_delete"
    FEED_HEADER_QUERY = "dke:feed_header_query"
    FEED_MESSAGE_QUERY = "dke:feed_message_query"
    CLOUD_ONBOARD_ENDPOINTS = "dke:cloud_onboard_endpoints"
    CLOUD_OFFBOARD_ENDPOINTS = "dke:cloud_offboard_endpoints"


class CapabilityType(BaseEnum):
    """
    Type of the capability.
    """

    ISO_11783_TASK_DATA_ZIP = "iso:11783:-10:taskdata:zip"
    ISO_11783_DEVICE_DESCRIPTION = "iso:11783:-10:device_description:protobuf"
    ISO_11783_TIMELOG = "iso:11783:-10:time_log:protobuf"
    IMG_BMP = "img:bmp"
    IMG_JPEG = "img:jpeg"
    IMG_PNG = "img:png"
    SHP_SHAPE_ZIP = "shp:shape:zip"
    DOC_PDF = "doc:pdf"
    VID_AVI = "vid:avi"
    VID_MP4 = "vid:mp4"
    VID_WMV = "vid:wmv"
    GPS_INFO = "gps:info"


class CapabilityDirectionType(BaseEnum):
    """
    Direction of the capability.
    """

    SEND = "SEND"
    RECEIVE = "RECEIVE"
    SEND_RECEIVE = "SEND_RECEIVE"


class CertificateTypes(BaseEnum):
    """
    CertificateTypes Enum Class

    An enum class representing different types of certificates.

    Attributes:
        PEM (str): The PEM certificate type.
        P12 (str): The P12 certificate type.
    """
    PEM = "PEM"
    P12 = "P12"


class Gateways(BaseEnum):
    """
    Enum class to store the possible gateways for communication.

    Attributes:
        MQTT (str): The MQTT gateway.
        HTTP (str): The HTTP gateway.
    """
    MQTT = "2"
    HTTP = "3"
