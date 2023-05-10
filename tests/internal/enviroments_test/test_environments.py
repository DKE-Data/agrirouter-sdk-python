"""Test agrirouter/environments/environments.py"""

from agrirouter.environments.environments import ProductionEnvironment as PE
from agrirouter.environments.environments import QAEnvironment as QAE
from tests.common.constants import APPLICATION_ID


class TestPE:
    def test_get_base_url(self):
        assert PE().get_base_url() == PE._ENV_BASE_URL

    def test_get_api_prefix(self):
        assert PE().get_api_prefix() == PE._API_PREFIX

    def test_get_registration_service_url(self):
        assert PE().get_registration_service_url() == PE._REGISTRATION_SERVICE_URL

    def test_get_onboard_url(self):
        onb_url = PE._REGISTRATION_SERVICE_URL + PE._API_PREFIX + "/registration/onboard"
        assert PE().get_onboard_url() == onb_url

    def test_get_secured_onboard_url(self):
        onb_url = PE._REGISTRATION_SERVICE_URL + PE._API_PREFIX + "/registration/onboard/request"
        assert PE().get_secured_onboard_url() == onb_url

    def test_get_verify_onboard_request_url(self):
        req_url = PE._REGISTRATION_SERVICE_URL + PE._API_PREFIX + "/registration/onboard/verify"
        assert PE().get_verify_onboard_request_url() == req_url

    def test_get_revoke_url(self):
        rev_url = PE._REGISTRATION_SERVICE_URL + PE._API_PREFIX + "/registration/onboard/revoke"
        assert PE().get_revoke_url() == rev_url

    def test_get_agrirouter_login_url(self):
        login_url = PE._ENV_BASE_URL + PE._AGRIROUTER_LOGIN_URL
        assert PE().get_agrirouter_login_url() == login_url

    def test_get_secured_onboarding_authorization_url(self):
        redirect_uri = "www.my_redirect.com"
        response_type = "response_type"
        assert PE().get_secured_onboarding_authorization_url(
            APPLICATION_ID, response_type, "state", redirect_uri
        ) == "https://goto.my-agrirouter.com/application/{application_id}/authorize?response_type={response_type}&state={state}".format( # noqa
            application_id=APPLICATION_ID,
            response_type=response_type,
            state="state") + f"&redirect_uri={redirect_uri}"

    def test_get_mqtt_server_url(self):
        assert PE().get_mqtt_server_url(
            "localhost", "5000"
        ) == PE._MQTT_URL_TEMPLATE.format(
            host="localhost", port="5000"
        )

    def test_get_env_public_key(self):
        assert PE().get_env_public_key() == PE.AR_PUBLIC_KEY


class TestQAE:
    def test_get_base_url(self):
        assert QAE().get_base_url() == QAE._ENV_BASE_URL

    def test_get_api_prefix(self):
        assert QAE().get_api_prefix() == QAE._API_PREFIX

    def test_get_registration_service_url(self):
        assert QAE().get_registration_service_url() == QAE._REGISTRATION_SERVICE_URL

    def test_get_onboard_url(self):
        onb_url = QAE._REGISTRATION_SERVICE_URL + QAE._API_PREFIX + "/registration/onboard"
        assert QAE().get_onboard_url() == onb_url

    def test_get_secured_onboard_url(self):
        onb_url = QAE._REGISTRATION_SERVICE_URL + QAE._API_PREFIX + "/registration/onboard/request"
        assert QAE().get_secured_onboard_url() == onb_url

    def test_get_verify_onboard_request_url(self):
        req_url = QAE._REGISTRATION_SERVICE_URL + QAE._API_PREFIX + "/registration/onboard/verify"
        assert QAE().get_verify_onboard_request_url() == req_url

    def test_get_revoke_url(self):
        rev_url = QAE._REGISTRATION_SERVICE_URL + QAE._API_PREFIX + "/registration/onboard/revoke"
        assert QAE().get_revoke_url() == rev_url

    def test_get_agrirouter_login_url(self):
        login_url = QAE._ENV_BASE_URL + QAE._AGRIROUTER_LOGIN_URL
        assert QAE().get_agrirouter_login_url() == login_url

    def test_get_secured_onboarding_authorization_url(self):
        redirect_uri = "www.my_redirect.com"
        response_type = "response_type"
        assert QAE().get_secured_onboarding_authorization_url(
            APPLICATION_ID, response_type, "state", redirect_uri
        ) == QAE._ENV_BASE_URL + QAE._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=APPLICATION_ID,
            response_type=response_type,
            state="state") + f"&redirect_uri={redirect_uri}"

    def test_get_mqtt_server_url(self):
        assert QAE().get_mqtt_server_url(
            "localhost", "5000"
        ) == QAE._MQTT_URL_TEMPLATE.format(host="localhost", port="5000")

    def test_get_env_public_key(self):
        assert QAE().get_env_public_key() == QAE.AR_PUBLIC_KEY
