from google.protobuf.any_pb2 import Any

from agrirouter.generated.commons.message_pb2 import Message, Messages
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope, RequestPayloadWrapper
from agrirouter.messaging.decode import DecodingService
from agrirouter.messaging.encode import write_proto_parts_to_buffer, EncodingService
from agrirouter.messaging.parameters.service import MessageHeaderParameters


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
    result = DecodingService.read_properties_buffers_from_input_stream(buffer)

    assert len(result) == 2
    assert len(result[0]) == envelope.ByteSize()
    assert len(result[1]) == payload.ByteSize()


def test_encode_header():
    """
    This test was created due to a Protobuf issue with Python >= 3.8, where
    `MergeFromString()` wouldn't accept lists as parameteres anymore.
    """
    message_header_parameters = MessageHeaderParameters()
    message_header_parameters.recipients = [
        "f1b3b3b3-7b3b-4b3b-b3b3-b3b3b3b3b3b3"
    ]
    message_header_parameters.application_message_id = "f1b3b3b3-7b3b-4b3b-b3b3-b3b3b3b3b3b3"
    message_header_parameters.application_message_seq_no = 1
    message_header_parameters.technical_message_type = "iso-11783-10:taskdata:zip"
    message_header_parameters.mode = RequestEnvelope.Mode.Value("DIRECT")

    header = EncodingService.encode_header(message_header_parameters)
    assert header.application_message_id == message_header_parameters.application_message_id
    assert header.application_message_seq_no == message_header_parameters.application_message_seq_no
    assert header.technical_message_type == message_header_parameters.technical_message_type
    assert header.mode == message_header_parameters.mode
    assert header.recipients == message_header_parameters.recipients
