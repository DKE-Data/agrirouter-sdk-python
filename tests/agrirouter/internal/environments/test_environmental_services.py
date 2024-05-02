"""Test src/env/environmental_services.py"""

from src.agrirouter.api.env import Qa, Production
from src.agrirouter.env.environmental_services import EnvironmentalService


def test_arclient_set_env():
    assert EnvironmentalService(env=Qa())._set_env(Qa()) is None
    assert EnvironmentalService(env=Production())._set_env(Production()) is None
