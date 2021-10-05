import base64
from ctypes import Union

from google.protobuf.any_pb2 import Any
from google.protobuf.internal.decoder import _DecodeVarint

from generated.commons.message_pb2 import Messages
from generated.messaging.response.payload.account.endpoints_pb2 import ListEndpointsResponse
from generated.messaging.response.payload.feed.feed_response_pb2 import HeaderQueryResponse, MessageQueryResponse
from generated.messaging.response.response_pb2 import ResponseEnvelope, ResponsePayloadWrapper
from messaging.messages import DecodedMessage


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

    envelope = ResponseEnvelope().MergeFromString(response_envelope_buffer)
    payload = ResponsePayloadWrapper().MergeFromString(response_payload_buffer)

    message = DecodedMessage(envelope, payload)

    return message


def decode_details(details: Any):
    if details.type_url == "Messages":
        return Messages().MergeFromString(details.value)
    elif details.type_url == "ListEndpointsResponse":
        return ListEndpointsResponse().MergeFromString(details.value)
    elif details.type_url == "HeaderQueryResponse":
        return HeaderQueryResponse().MergeFromString(details.value)
    elif details.type_url == "MessageQueryResponse":
        return MessageQueryResponse().MergeFromString(details.value)
