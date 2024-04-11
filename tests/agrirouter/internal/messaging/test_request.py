"""Test src/messaging/request.py"""

from src.agrirouter.messaging.messages import Message
from src.agrirouter.messaging.request import MessageRequest


def test_json_serialize():
    message_request = MessageRequest(
        sensor_alternate_id="1",
        capability_alternate_id="1",
        messages=[Message(content="content")],
    ).json_serialize()
    assert message_request["capabilityAlternateId"] == "1"
    assert message_request["sensorAlternateId"] == "1"
    assert message_request["measures"]
