import json

import pytest

from agrirouter.messaging.decode import decode_response
from agrirouter.messaging.decode import decode_details


MESSAGING_RESULT = b'[{"sensorAlternateId":"185cd97b-ed0b-4e75-a6e2-6be1cdd38a06","capabilityAlternateId":"bbe9f361-b551-48d9-9fca-1b4dc768287c","command":{"message":"XwjIARAKGiQ5NWUzNWE0Zi1jNWM4LTQ1NDEtODE4OS03NmJlMzM0OTc0NDUiJDUzNzYyM2ZjLWY2NmYtNDc5Yi1hMmJhLWVjZjNlNWM3ZjhlMCoMCNTV5YsGEICI8LIDzQIKygIKTnR5cGVzLmFncmlyb3V0ZXIuY29tL2Fncmlyb3V0ZXIucmVzcG9uc2UucGF5bG9hZC5hY2NvdW50Lkxpc3RFbmRwb2ludHNSZXNwb25zZRL3AQp4CiRkNzA0YTQ0My05OWY3LTQ3YjQtYmU1NS1lMmZhMDk2ODllYmUSJFB5dGhvblNES19kZXYgLSAyMDIxLTEwLTI1LCAxMDo1MToxOBoLYXBwbGljYXRpb24iBmFjdGl2ZTIVdXJuOm15YXBwOnNucjAwMDAzMjM0CnsKJDE4NWNkOTdiLWVkMGItNGU3NS1hNmUyLTZiZTFjZGQzOGEwNhIkUHl0aG9uU0RLX2RldiAtIDIwMjEtMTAtMjEsIDIxOjQxOjI0GgthcHBsaWNhdGlvbiIGYWN0aXZlMhh1cm46bXlhcHA6c25yMDAwMDMyMzRzZGY="}}]'


def test_decode_response():
    pass


def test_decode_details():
    json_response = json.loads(MESSAGING_RESULT)
    message = decode_response(json_response[0]["command"]["message"].encode())
    decoded_details = decode_details(message.response_payload.details)
    print(decoded_details)
    assert False
