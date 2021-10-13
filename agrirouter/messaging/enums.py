from agrirouter.auth.enums import BaseEnum


class TechnicalMessageType(BaseEnum):
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
