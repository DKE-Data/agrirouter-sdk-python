from google.protobuf.any_pb2 import Any

from agrirouter.generated.commons.message_pb2 import Message, Messages
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope, RequestPayloadWrapper
from agrirouter.messaging.decode import read_properties_buffers_from_input_stream
from agrirouter.messaging.encode import write_proto_parts_to_buffer


def test_write_proto_parts_to_buffer():
    mode = 1
    tmt = "TMT"
    team_set_context_id = "team_set_context_id"
    type_url = "type_url"

    message = Message(message="Test message", message_code="Test message code")
    messages = Messages(messages=[message])

    envelope = RequestEnvelope(mode=mode, technical_message_type=tmt, team_set_context_id=team_set_context_id)
    payload = RequestPayloadWrapper(details=Any(type_url=type_url, value=messages.SerializeToString()))

    buffer = write_proto_parts_to_buffer([envelope, payload])
    result = read_properties_buffers_from_input_stream(buffer)

    assert len(result) == 2
    assert len(result[0]) == envelope.ByteSize()
    assert len(result[1]) == payload.ByteSize()
