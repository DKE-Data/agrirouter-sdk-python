import json

from agrirouter.generated.messaging.response.response_pb2 import ResponseEnvelope
from agrirouter.service.messaging.decoding import DecodingService

MESSAGING_RESULT = b'[{"sensorAlternateId":"185cd97b-ed0b-4e75-a6e2-6be1cdd38a06","capabilityAlternateId":"bbe9f361-b551-48d9-9fca-1b4dc768287c","command":{"message":"XwjIARAKGiQ5NWUzNWE0Zi1jNWM4LTQ1NDEtODE4OS03NmJlMzM0OTc0NDUiJDUzNzYyM2ZjLWY2NmYtNDc5Yi1hMmJhLWVjZjNlNWM3ZjhlMCoMCNTV5YsGEICI8LIDzQIKygIKTnR5cGVzLmFncmlyb3V0ZXIuY29tL2Fncmlyb3V0ZXIucmVzcG9uc2UucGF5bG9hZC5hY2NvdW50Lkxpc3RFbmRwb2ludHNSZXNwb25zZRL3AQp4CiRkNzA0YTQ0My05OWY3LTQ3YjQtYmU1NS1lMmZhMDk2ODllYmUSJFB5dGhvblNES19kZXYgLSAyMDIxLTEwLTI1LCAxMDo1MToxOBoLYXBwbGljYXRpb24iBmFjdGl2ZTIVdXJuOm15YXBwOnNucjAwMDAzMjM0CnsKJDE4NWNkOTdiLWVkMGItNGU3NS1hNmUyLTZiZTFjZGQzOGEwNhIkUHl0aG9uU0RLX2RldiAtIDIwMjEtMTAtMjEsIDIxOjQxOjI0GgthcHBsaWNhdGlvbiIGYWN0aXZlMhh1cm46bXlhcHA6c25yMDAwMDMyMzRzZGY="}}]'  # noqa


def test_decode_response():
    json_response = json.loads(MESSAGING_RESULT)
    message = DecodingService.decode_response(json_response[0]["command"]["message"].encode())
    assert message.response_payload
    assert message.response_envelope

    assert message.response_payload.details

    assert message.response_payload.details.type_url == "types.agrirouter.com/agrirouter.response.payload.account.ListEndpointsResponse"  # noqa
    assert message.response_payload.details.value == b'\nx\n$d704a443-99f7-47b4-be55-e2fa09689ebe\x12$PythonSDK_dev - 2021-10-25, 10:51:18\x1a\x0bapplication"\x06active2\x15urn:myapp:snr00003234\n{\n$185cd97b-ed0b-4e75-a6e2-6be1cdd38a06\x12$PythonSDK_dev - 2021-10-21, 21:41:24\x1a\x0bapplication"\x06active2\x18urn:myapp:snr00003234sdf'  # noqa

    assert message.response_envelope.response_code == 200
    assert message.response_envelope.type == ResponseEnvelope.ResponseBodyType.Value("ENDPOINTS_LISTING")
    assert message.response_envelope.application_message_id == "95e35a4f-c5c8-4541-8189-76be33497445"
    assert message.response_envelope.message_id == "537623fc-f66f-479b-a2ba-ecf3e5c7f8e0"

    assert message.response_envelope.timestamp
    assert message.response_envelope.timestamp.seconds == 1635347156
    assert message.response_envelope.timestamp.nanos == 912000000


def test_decode_details():
    json_response = json.loads(MESSAGING_RESULT)
    message = DecodingService.decode_response(json_response[0]["command"]["message"].encode())
    details = message.response_payload.details
    decoded_details = decode_details(details)

    assert decoded_details.endpoints
    assert len(decoded_details.endpoints) == 2
    assert decoded_details.endpoints[0].endpoint_id == "d704a443-99f7-47b4-be55-e2fa09689ebe"
    assert decoded_details.endpoints[0].endpoint_name == "PythonSDK_dev - 2021-10-25, 10:51:18"
    assert decoded_details.endpoints[0].endpoint_type == "application"
    assert decoded_details.endpoints[0].status == "active"
    assert decoded_details.endpoints[0].external_id == "urn:myapp:snr00003234"

    assert decoded_details.endpoints[1].endpoint_id == "185cd97b-ed0b-4e75-a6e2-6be1cdd38a06"
    assert decoded_details.endpoints[1].endpoint_name == "PythonSDK_dev - 2021-10-21, 21:41:24"
    assert decoded_details.endpoints[1].endpoint_type == "application"
    assert decoded_details.endpoints[1].status == "active"
    assert decoded_details.endpoints[1].external_id == "urn:myapp:snr00003234sdf"
