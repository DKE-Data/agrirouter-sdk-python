"""Test agrirouter/environments/environmental_services.py"""

import pytest
from agrirouter.environments.exceptions import InvalidEnvironmentSetup
from agrirouter.environments.environmental_services import EnvironmentalService
from tests.constants import ENV


def test_arclient_set_env():
    assert isinstance(EnvironmentalService("Production")._set_env("Production"), object)
    assert isinstance(EnvironmentalService(ENV)._set_env(ENV), object)
    with pytest.raises(InvalidEnvironmentSetup):
        assert EnvironmentalService("WRONG")._set_env("WRONG")
