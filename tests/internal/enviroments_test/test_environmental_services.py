"""Test agrirouter/environments/environmental_services.py"""

import pytest

from agrirouter.api.enums import Environments
from agrirouter.api.exceptions import InvalidEnvironmentSetup
from agrirouter.environments.environmental_services import EnvironmentalService
from tests.common.constants import ENV


def test_arclient_set_env():
    assert EnvironmentalService(ENV)._set_env(ENV) is None
    assert EnvironmentalService(env=Environments.PRODUCTION.value)._set_env(Environments.PRODUCTION.value) is None
    with pytest.raises(InvalidEnvironmentSetup):
        assert EnvironmentalService("WRONG")._set_env("WRONG")
