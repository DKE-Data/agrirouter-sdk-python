"""Test agrirouter/environments/environmental_services.py"""

import pytest
from agrirouter.environments.exceptions import InvalidEnvironmentSetup
from agrirouter.environments.environmental_services import EnvironmentalService
from tests.constants import ENV


def test_arclient_set_env():
    with pytest.raises(InvalidEnvironmentSetup):
        assert EnvironmentalService("WRONG")._set_env("WRONG")
