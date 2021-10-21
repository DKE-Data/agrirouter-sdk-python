"""Test agrirouter/onboarding/signature.py"""

import pytest
import re
from agrirouter.onboarding.signature import create_signature
from tests.constants import private_key, wrong_private_key


def test_create_signature():
    assert re.search(r"[\w]", create_signature("127.0.0.1", private_key))
    with pytest.raises(ValueError):
        assert re.search(r"[\w]", create_signature("127.0.0.1", wrong_private_key))
