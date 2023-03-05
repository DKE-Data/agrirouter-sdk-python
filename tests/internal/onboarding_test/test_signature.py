"""Test agrirouter/onboarding/signature.py"""

import pytest

from cryptography.exceptions import InvalidSignature

from agrirouter.onboarding.signature import create_signature, verify_signature
from tests.constants import private_key, public_key


def test_create_signature_ok():
    signature = create_signature(
        "REQUEST CONTENT", private_key)
    raised = False
    try:
        verify_signature(
            "REQUEST CONTENT", bytes.fromhex(signature), public_key)
    except InvalidSignature:
        raised = True
    assert not raised


def test_verify_signature_fail():
    with pytest.raises(InvalidSignature):
        verify_signature(
            "REQUEST CONTENT", b"wrong_signature", public_key)
