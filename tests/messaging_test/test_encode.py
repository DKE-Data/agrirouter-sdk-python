"""Test agrirouter/messaging/encode.py"""

from agrirouter.messaging.encode import write_proto_parts_to_buffer


def test_write_proto_parts_to_buffer():
    assert write_proto_parts_to_buffer([], b"test_message") == b"test_message"
