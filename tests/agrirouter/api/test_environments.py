import unittest

from src.agrirouter.api import environments


class TestEnvironments(unittest.TestCase):
    def test_get_base_url(self):
        env = environments.BaseEnvironment()
        assert env.get_base_url() == ""

    def test_get_api_prefix(self):
        env = environments.BaseEnvironment()
        assert env.get_api_prefix() == ""

    def test_get_registration_service_url(self):
        env = environments.BaseEnvironment()
        assert env.get_registration_service_url() == ""

    def test_get_onboard_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/registration/onboard"
        assert env.get_onboard_url() == expected_url

    def test_get_secured_onboard_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/registration/onboard/request"
        assert env.get_secured_onboard_url() == expected_url

    def test_get_verify_onboard_request_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/registration/onboard/verify"
        assert env.get_verify_onboard_request_url() == expected_url

    def test_get_revoke_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/registration/onboard/revoke"
        assert env.get_revoke_url() == expected_url

    def test_get_agrirouter_login_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/app"
        assert env.get_agrirouter_login_url() == expected_url

    def test_get_secured_onboarding_authorization_url(self):
        env = environments.BaseEnvironment()
        expected_url = "/application/test_app/authorize?response_type=test_response_type&state=test_state&redirect_uri=test_redirect_uri"  # noqa
        assert env.get_secured_onboarding_authorization_url("test_app", "test_response_type", "test_state",  # noqa
                                                            "test_redirect_uri") == expected_url

    def test_get_mqtt_server_url(self):
        env = environments.BaseEnvironment()
        expected_url = "ssl://test_host:test_port"
        assert env.get_mqtt_server_url("test_host", "test_port") == expected_url

    def test_get_env_public_key(self):
        env = environments.BaseEnvironment()
        assert env.get_env_public_key() is None
