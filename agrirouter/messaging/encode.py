import base64

from google.protobuf.any_pb2 import Any
from google.protobuf.internal.encoder import _VarintBytes

from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope, RequestPayloadWrapper

from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters
from agrirouter.utils.utc_time_util import now_as_utc_timestamp
from agrirouter.utils.uuid_util import new_uuid


def write_proto_parts_to_buffer(parts: list, buffer: bytes = b""):
    for part in parts:
        part_size = part.ByteSize()
        buffer += _VarintBytes(part_size)
        buffer += part.SerializeToString()

    return buffer


def encode_message(header_parameters: MessageHeaderParameters, payload_parameters: MessagePayloadParameters) -> str:
    request_envelope = encode_header(header_parameters)
    request_payload = encode_payload(payload_parameters)

    raw_data = write_proto_parts_to_buffer([request_envelope, request_payload])

    return base64.b64encode(raw_data).decode()


def encode_header(header_parameters: MessageHeaderParameters) -> RequestEnvelope:
    request_envelope = RequestEnvelope()
    request_envelope.application_message_id = header_parameters.get_application_message_id() \
        if header_parameters.get_application_message_id() else new_uuid()
    request_envelope.application_message_seq_no = header_parameters.get_application_message_seq_no()
    request_envelope.technical_message_type = header_parameters.get_technical_message_type()
    request_envelope.mode = header_parameters.get_mode()
    if header_parameters.get_team_set_context_id() is not None:
        request_envelope.team_set_context_id = header_parameters.get_team_set_context_id()
    request_envelope.timestamp.FromDatetime(now_as_utc_timestamp())
    if header_parameters.get_recipients() is not None:
        request_envelope.recipients.MergeFrom(header_parameters.get_recipients())
    if header_parameters.get_chunk_component() is not None:
        request_envelope.chunk_info.MergeFrom(header_parameters.get_chunk_component())
    if header_parameters.get_metadata() is not None:
        request_envelope.metadata.MergeFrom(header_parameters.get_metadata())

    return request_envelope


def encode_payload(payload_parameters: MessagePayloadParameters) -> RequestPayloadWrapper:
    any_proto_wrapper = Any()
    any_proto_wrapper.type_url = payload_parameters.get_type_url()
    any_proto_wrapper.value = payload_parameters.get_value()
    request_payload = RequestPayloadWrapper(details=any_proto_wrapper)
    return request_payload
