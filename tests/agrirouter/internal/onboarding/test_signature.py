"""Test agrirouter/onboarding/signature.py"""

import pytest
from cryptography.exceptions import InvalidSignature

from agrirouter.onboarding.signature import SignatureService
from tests.agrirouter.common.constants import PRIVATE_KEY, PUBLIC_KEY


def test_create_signature_ok():
    signature = SignatureService.create_signature(
        "REQUEST CONTENT", PRIVATE_KEY)
    raised = False
    try:
        SignatureService.verify_signature(
            "REQUEST CONTENT", bytes.fromhex(signature), PUBLIC_KEY)
    except InvalidSignature:
        raised = True
    assert not raised


def test_verify_signature_fail():
    with pytest.raises(InvalidSignature):
        SignatureService.verify_signature(
            "REQUEST CONTENT", b"wrong_signature", PUBLIC_KEY)
