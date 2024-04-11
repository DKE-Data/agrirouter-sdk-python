"""Test src/environments/environments.py"""

from src.api.environments import Production
from src.api.environments import Qa
from tests.common.constants import APPLICATION_ID


class TestProduction:
    def test_get_base_url(self):
        assert Production().get_base_url() == Production._ENV_BASE_URL

    def test_get_api_prefix(self):
        assert Production().get_api_prefix() == Production._API_PREFIX

    def test_get_registration_service_url(self):
        assert Production().get_registration_service_url() == Production._REGISTRATION_SERVICE_URL

    def test_get_onboard_url(self):
        onb_url = Production._REGISTRATION_SERVICE_URL + Production._API_PREFIX + "/registration/onboard"
        assert Production().get_onboard_url() == onb_url

    def test_get_secured_onboard_url(self):
        onb_url = Production._REGISTRATION_SERVICE_URL + Production._API_PREFIX + "/registration/onboard/request"
        assert Production().get_secured_onboard_url() == onb_url

    def test_get_verify_onboard_request_url(self):
        req_url = Production._REGISTRATION_SERVICE_URL + Production._API_PREFIX + "/registration/onboard/verify"
        assert Production().get_verify_onboard_request_url() == req_url

    def test_get_revoke_url(self):
        rev_url = Production._REGISTRATION_SERVICE_URL + Production._API_PREFIX + "/registration/onboard/revoke"
        assert Production().get_revoke_url() == rev_url

    def test_get_agrirouter_login_url(self):
        login_url = Production._ENV_BASE_URL + Production._LOGIN_URL
        assert Production().get_agrirouter_login_url() == login_url

    def test_get_secured_onboarding_authorization_url(self):
        redirect_uri = "www.my_redirect.com"
        response_type = "response_type"
        assert Production().get_secured_onboarding_authorization_url(
            APPLICATION_ID, response_type, "state", redirect_uri
        ) == ("https://goto.my-agrirouter.com/application/{application_id}/"
              "authorize?response_type={response_type}&state={state}").format(
            # noqa
            application_id=APPLICATION_ID,
            response_type=response_type,
            state="state") + f"&redirect_uri={redirect_uri}"

    def test_get_mqtt_server_url(self):
        assert Production().get_mqtt_server_url(
            "localhost", "5000"
        ) == Production._MQTT_URL_TEMPLATE.format(
            host="localhost", port="5000"
        )

    def test_get_env_public_key(self):
        assert Production().get_env_public_key() == Production._AR_PUBLIC_KEY


class TestQa:
    def test_get_base_url(self):
        assert Qa().get_base_url() == Qa._ENV_BASE_URL

    def test_get_api_prefix(self):
        assert Qa().get_api_prefix() == Qa._API_PREFIX

    def test_get_registration_service_url(self):
        assert Qa().get_registration_service_url() == Qa._REGISTRATION_SERVICE_URL

    def test_get_onboard_url(self):
        onb_url = Qa._REGISTRATION_SERVICE_URL + Qa._API_PREFIX + "/registration/onboard"
        assert Qa().get_onboard_url() == onb_url

    def test_get_secured_onboard_url(self):
        onb_url = Qa._REGISTRATION_SERVICE_URL + Qa._API_PREFIX + "/registration/onboard/request"
        assert Qa().get_secured_onboard_url() == onb_url

    def test_get_verify_onboard_request_url(self):
        req_url = Qa._REGISTRATION_SERVICE_URL + Qa._API_PREFIX + "/registration/onboard/verify"
        assert Qa().get_verify_onboard_request_url() == req_url

    def test_get_revoke_url(self):
        rev_url = Qa._REGISTRATION_SERVICE_URL + Qa._API_PREFIX + "/registration/onboard/revoke"
        assert Qa().get_revoke_url() == rev_url

    def test_get_agrirouter_login_url(self):
        login_url = Qa._ENV_BASE_URL + Qa._LOGIN_URL
        assert Qa().get_agrirouter_login_url() == login_url

    def test_get_secured_onboarding_authorization_url(self):
        redirect_uri = "www.my_redirect.com"
        response_type = "response_type"
        assert Qa().get_secured_onboarding_authorization_url(
            APPLICATION_ID, response_type, "state", redirect_uri
        ) == Qa._ENV_BASE_URL + Qa._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=APPLICATION_ID,
            response_type=response_type,
            state="state") + f"&redirect_uri={redirect_uri}"

    def test_get_mqtt_server_url(self):
        assert Qa().get_mqtt_server_url(
            "localhost", "5000"
        ) == Qa._MQTT_URL_TEMPLATE.format(host="localhost", port="5000")

    def test_get_env_public_key(self):
        assert Qa().get_env_public_key() == Qa._AR_PUBLIC_KEY
