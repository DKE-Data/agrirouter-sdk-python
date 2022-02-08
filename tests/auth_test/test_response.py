"""Tests agrirouter/auth/response.py"""

import re

import pytest

from agrirouter.auth.response import AuthResponse
from tests.constants import valid_response_signature, valid_response_token, AR_PUBLIC_KEY


def test_decode_token():

    decoded_token = AuthResponse.decode_token(valid_response_token)
    assert re.search(r"[\w]", decoded_token.regcode)
    assert re.search(r"[\w]", decoded_token.account)
    assert decoded_token.expires


def test_verify(authorization):
    state = "46c81f94-d117-4658-9a38-a85692448219"
    token = valid_response_token
    signature = valid_response_signature

    auth_response = AuthResponse({"state": state,
                                  "signature": signature,
                                  "token": token})

    assert auth_response.signature
    assert auth_response.token
    assert not auth_response.error

    with pytest.raises(PermissionError):
        auth_response.is_valid
    auth_response.verify(AR_PUBLIC_KEY)
    assert auth_response.is_valid


def test_get_auth_result(authorization):
    state = "46c81f94-d117-4658-9a38-a85692448219"
    token = valid_response_token
    signature = valid_response_signature

    auth_response = AuthResponse({"state": state,
                                  "signature": signature,
                                  "token": token})

    auth_result = auth_response.get_auth_result()

    assert auth_result.token == token
    assert auth_result.state == state
    assert auth_result.signature == signature
    assert not auth_result.error
    assert auth_result.decoded_token

    assert re.search(r"[\w]", auth_result.decoded_token.regcode)
    assert re.search(r"[\w]", auth_result.decoded_token.account)
    assert auth_result.decoded_token.expires
