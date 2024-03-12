"""Test agrirouter/environments/environmental_services.py"""

import pytest

from agrirouter.environments.environmental_services import EnvironmentalService
from agrirouter.api.exceptions import InvalidEnvironmentSetup
from tests.common.constants import ENV


def test_arclient_set_env():
    assert EnvironmentalService(ENV)._set_env(ENV) is None
    assert EnvironmentalService("Production")._set_env("Production") is None
    with pytest.raises(InvalidEnvironmentSetup):
        assert EnvironmentalService("WRONG")._set_env("WRONG")
