"""Test agrirouter/environments/environmental_services.py"""

import pytest
from agrirouter.environments.exceptions import InvalidEnvironmentSetup
from agrirouter.environments.environmental_services import EnvironmentalService
from tests.constants import env


def test_arclient_set_env():
    assert EnvironmentalService(env)._set_env(env) is None
    assert EnvironmentalService("Production")._set_env("Production") is None
    with pytest.raises(InvalidEnvironmentSetup):
        assert EnvironmentalService("WRONG")._set_env("WRONG")
