"""Tests agrirouter/auth/response.py"""
import base64
import re
from agrirouter.auth.response import AuthResponse


def test_decode_token():
    token = (
        "eyJhY2NvdW50IjoiMGJhMjRlZWUtYzMwYi00N2U1LWJkYzktNzcwM"
        "2NmYjEzNmEwIiwicmVnY29kZSI6IjhlYWNiMTk4ZmMiLCJleHBpcm"
        "VzIjoiMjAyMS0wOS0yM1QxNjowODo0My44ODhaIn0="
    )
    decoded_token = AuthResponse.decode_token(token)
    assert isinstance(decoded_token["account"], str)
    assert isinstance(decoded_token["expires"], str)
    assert re.search(r"[\w]", decoded_token["regcode"])
    assert re.search(r"[\w]", decoded_token["account"])


def test_get_auth_result(authorization):
    assert isinstance(AuthResponse(authorization).get_auth_result(), dict)
    assert AuthResponse(authorization).get_auth_result()["credentials"]
