"""Test agrirouter/environments/environments.py"""

import pytest
from agrirouter.environments.environments import ProductionEnvironment, QAEnvironment
from tests.constants import application_id, auth_result_url


class TestProductionEnvironment:
    def test_get_base_url(self):
        assert (
            ProductionEnvironment().get_base_url()
            == ProductionEnvironment._ENV_BASE_URL
        )

    def test_get_api_prefix(self):
        assert (
            ProductionEnvironment().get_api_prefix()
            == ProductionEnvironment._API_PREFIX
        )

    def test_get_registration_service_url(self):
        assert (
            ProductionEnvironment().get_registration_service_url()
            == ProductionEnvironment._REGISTRATION_SERVICE_URL
        )

    def test_get_onboard_url(self):
        assert (
            ProductionEnvironment().get_onboard_url()
            == ProductionEnvironment._REGISTRATION_SERVICE_URL
            + ProductionEnvironment._API_PREFIX
            + "/registration/onboard"
        )

    def test_get_secured_onboard_url(self):
        assert (
            ProductionEnvironment().get_secured_onboard_url()
            == ProductionEnvironment._REGISTRATION_SERVICE_URL
            + ProductionEnvironment._API_PREFIX
            + "/registration/onboard/request"
        )

    def test_get_verify_onboard_request_url(self):
        assert (
            ProductionEnvironment().get_verify_onboard_request_url()
            == ProductionEnvironment._REGISTRATION_SERVICE_URL
            + ProductionEnvironment._API_PREFIX
            + "/registration/onboard/verify"
        )

    def test_get_revoke_url(self):
        assert (
            ProductionEnvironment().get_revoke_url()
            == ProductionEnvironment._REGISTRATION_SERVICE_URL
            + ProductionEnvironment._API_PREFIX
            + "/registration/onboard/revoke"
        )

    def test_get_agrirouter_login_url(self):
        assert (
            ProductionEnvironment().get_agrirouter_login_url()
            == ProductionEnvironment._ENV_BASE_URL
            + ProductionEnvironment._AGRIROUTER_LOGIN_URL
        )

    def test_get_secured_onboarding_authorization_url(self):
        assert ProductionEnvironment().get_secured_onboarding_authorization_url(
            application_id, str, "state", auth_result_url
        ) == ProductionEnvironment._ENV_BASE_URL + ProductionEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=application_id,
            response_type=str,
            state="state",
            redirect_uri=auth_result_url,
        )
        with pytest.raises(AssertionError):
            assert ProductionEnvironment().get_secured_onboarding_authorization_url(
                application_id, str, "state", auth_result_url
            ) == ProductionEnvironment._ENV_BASE_URL + ProductionEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
                application_id=application_id,
                response_type=str,
                state="123",
                redirect_uri=auth_result_url,
            )
        with pytest.raises(AssertionError):
            assert ProductionEnvironment().get_secured_onboarding_authorization_url(
                application_id, dict, "state", auth_result_url
            ) == ProductionEnvironment._ENV_BASE_URL + ProductionEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
                application_id=application_id,
                response_type=str,
                state="state",
                redirect_uri=auth_result_url,
            )

    def test_get_mqtt_server_url(self):
        assert ProductionEnvironment().get_mqtt_server_url(
            "localhost", "5000"
        ) == ProductionEnvironment._MQTT_URL_TEMPLATE.format(
            host="localhost", port="5000"
        )
        with pytest.raises(AssertionError):
            assert ProductionEnvironment().get_mqtt_server_url(
                "localhost", "5000"
            ) == ProductionEnvironment._MQTT_URL_TEMPLATE.format(
                host="127.0.0.1", port="5000"
            )
        with pytest.raises(AssertionError):
            assert ProductionEnvironment().get_mqtt_server_url(
                "localhost", "5000"
            ) == ProductionEnvironment._MQTT_URL_TEMPLATE.format(
                host="localhost", port="80"
            )

    def test_get_env_public_key(self):
        assert (
            ProductionEnvironment().get_env_public_key()
            == ProductionEnvironment.AR_PUBLIC_KEY
        )


class TestQAEnvironment:
    def test_get_base_url(self):
        assert QAEnvironment().get_base_url() == QAEnvironment._ENV_BASE_URL

    def test_get_api_prefix(self):
        assert QAEnvironment().get_api_prefix() == QAEnvironment._API_PREFIX

    def test_get_registration_service_url(self):
        assert (
            QAEnvironment().get_registration_service_url()
            == QAEnvironment._REGISTRATION_SERVICE_URL
        )

    def test_get_onboard_url(self):
        assert (
            QAEnvironment().get_onboard_url()
            == QAEnvironment._REGISTRATION_SERVICE_URL
            + QAEnvironment._API_PREFIX
            + "/registration/onboard"
        )

    def test_get_secured_onboard_url(self):
        assert (
            QAEnvironment().get_secured_onboard_url()
            == QAEnvironment._REGISTRATION_SERVICE_URL
            + QAEnvironment._API_PREFIX
            + "/registration/onboard/request"
        )

    def test_get_verify_onboard_request_url(self):
        assert (
            QAEnvironment().get_verify_onboard_request_url()
            == QAEnvironment._REGISTRATION_SERVICE_URL
            + QAEnvironment._API_PREFIX
            + "/registration/onboard/verify"
        )

    def test_get_revoke_url(self):
        assert (
            QAEnvironment().get_revoke_url()
            == QAEnvironment._REGISTRATION_SERVICE_URL
            + QAEnvironment._API_PREFIX
            + "/registration/onboard/revoke"
        )

    def test_get_agrirouter_login_url(self):
        assert (
            QAEnvironment().get_agrirouter_login_url()
            == QAEnvironment._ENV_BASE_URL + QAEnvironment._AGRIROUTER_LOGIN_URL
        )

    def test_get_secured_onboarding_authorization_url(self):
        assert QAEnvironment().get_secured_onboarding_authorization_url(
            application_id, str, "state", auth_result_url
        ) == QAEnvironment._ENV_BASE_URL + QAEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=application_id,
            response_type=str,
            state="state",
            redirect_uri=auth_result_url,
        )
        with pytest.raises(AssertionError):
            assert QAEnvironment().get_secured_onboarding_authorization_url(
                application_id, str, "state", auth_result_url
            ) == QAEnvironment._ENV_BASE_URL + QAEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
                application_id=application_id,
                response_type=str,
                state="123",
                redirect_uri=auth_result_url,
            )
        with pytest.raises(AssertionError):
            assert QAEnvironment().get_secured_onboarding_authorization_url(
                application_id, dict, "state", auth_result_url
            ) == QAEnvironment._ENV_BASE_URL + QAEnvironment._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
                application_id=application_id,
                response_type=str,
                state="state",
                redirect_uri=auth_result_url,
            )

    def test_get_mqtt_server_url(self):
        assert QAEnvironment().get_mqtt_server_url(
            "localhost", "5000"
        ) == QAEnvironment._MQTT_URL_TEMPLATE.format(host="localhost", port="5000")
        with pytest.raises(AssertionError):
            assert QAEnvironment().get_mqtt_server_url(
                "localhost", "5000"
            ) == QAEnvironment._MQTT_URL_TEMPLATE.format(host="127.0.0.1", port="5000")
        with pytest.raises(AssertionError):
            assert QAEnvironment().get_mqtt_server_url(
                "localhost", "5000"
            ) == QAEnvironment._MQTT_URL_TEMPLATE.format(host="localhost", port="80")

    def test_get_env_public_key(self):
        assert QAEnvironment().get_env_public_key() == QAEnvironment.AR_PUBLIC_KEY
