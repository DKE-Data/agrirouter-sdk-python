import base64

from google.protobuf.any_pb2 import Any
from google.protobuf.internal.decoder import _DecodeVarint

from agrirouter.generated.commons.message_pb2 import Messages
from agrirouter.generated.messaging.response.payload.account.endpoints_pb2 import ListEndpointsResponse
from agrirouter.generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse, \
    MessageQueryResponse
from agrirouter.generated.messaging.response.payload.feed.push_notification_pb2 import PushNotification
from agrirouter.generated.messaging.response.response_pb2 import ResponseEnvelope, ResponsePayloadWrapper
from agrirouter.messaging.exceptions import DecodeMessageException
from agrirouter.messaging.messages import DecodedMessage
from agrirouter.utils.type_url import TypeUrl


def read_properties_buffers_from_input_stream(input_stream) -> tuple:
    result = []
    pos = 0
    while pos < len(input_stream):
        msg_len, pos = _DecodeVarint(input_stream, pos)

        msg_buf = input_stream[pos:pos + msg_len]
        result.append(msg_buf)

        pos += msg_len

    return tuple(result)


def decode_response(message: bytes) -> DecodedMessage:
    input_stream = base64.b64decode(message)
    response_envelope_buffer, response_payload_buffer = read_properties_buffers_from_input_stream(input_stream)

    envelope = ResponseEnvelope()
    envelope.ParseFromString(response_envelope_buffer)
    payload = ResponsePayloadWrapper()
    payload.ParseFromString(response_payload_buffer)

    message = DecodedMessage(envelope, payload)

    return message


def decode_details(details: Any):
    if details.type_url == TypeUrl.get_type_url(Messages):
        messages = Messages()
        messages.MergeFromString(details.value)
        return messages
    elif details.type_url == TypeUrl.get_type_url(ListEndpointsResponse):
        list_endpoints_response = ListEndpointsResponse()
        list_endpoints_response.MergeFromString(details.value)
        return list_endpoints_response
    elif details.type_url == TypeUrl.get_type_url(HeaderQueryResponse):
        header_query_response = HeaderQueryResponse()
        header_query_response.MergeFromString(details.value)
        return header_query_response
    elif details.type_url == TypeUrl.get_type_url(MessageQueryResponse):
        message_query_response = MessageQueryResponse()
        message_query_response.MergeFromString(details.value)
        return message_query_response
    elif details.type_url == TypeUrl.get_type_url(PushNotification):
        pushnotification = PushNotification()
        pushnotification.MergeFromString(details.value)
        return pushnotification
    else:
        raise DecodeMessageException(f"Could not handle type {details.type_url} while decoding details.")
