from environments.keys import AR_QA_PUBLIC_KEY, AR_PROD_PUBLIC_KEY


class BaseEnvironment:
    _AGRIROUTER_LOGIN_URL = "/app"
    _MQTT_URL_TEMPLATE = "ssl://{host}:{port}"
    _SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE = \
        "/application/{application_id}/authorize" \
        "?response_type={response_type}&state={state}&redirect_uri={redirect_uri}"

    _ENV_BASE_URL = ""
    _API_PREFIX = ""
    _REGISTRATION_SERVICE_URL = ""

    AR_PUBLIC_KEY = None

    def get_base_url(self) -> str:
        return self._ENV_BASE_URL

    def get_api_prefix(self) -> str:
        return self._API_PREFIX

    def get_registration_service_url(self) -> str:
        return self._REGISTRATION_SERVICE_URL

    def get_onboard_url(self) -> str:
        return self.get_registration_service_url() + self.get_api_prefix() + "/registration/onboard"

    def get_secured_onboard_url(self) -> str:
        return self.get_registration_service_url() + self.get_api_prefix() + "/registration/onboard/request"

    def get_verify_onboard_request_url(self) -> str:
        return self.get_registration_service_url() + self.get_api_prefix() + "/registration/onboard/verify"

    def get_revoke_url(self) -> str:
        return self.get_registration_service_url() + self.get_api_prefix() + "/registration/onboard/revoke"

    def get_agrirouter_login_url(self) -> str:
        return self.get_base_url() + self._AGRIROUTER_LOGIN_URL

    def get_secured_onboarding_authorization_url(self, application_id, response_type, state, redirect_uri) -> str:
        return self.get_base_url() + self._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=application_id,
            response_type=response_type,
            state=state,
            redirect_uri=redirect_uri
        )

    def get_mqtt_server_url(self, host, port) -> str:
        return self._MQTT_URL_TEMPLATE.format(host=host, port=port)

    def get_env_public_key(self):
        return self.AR_PUBLIC_KEY


class ProductionEnvironment(BaseEnvironment):
    _ENV_BASE_URL = "https://goto.my-agrirouter.com"
    _API_PREFIX = "/api/v1.0"
    _REGISTRATION_SERVICE_URL = "https://onboard.my-agrirouter.com"

    AR_PUBLIC_KEY = AR_PROD_PUBLIC_KEY


class QAEnvironment(BaseEnvironment):
    _ENV_BASE_URL = "https://agrirouter-qa.cfapps.eu10.hana.ondemand.com"
    _API_PREFIX = "/api/v1.0"
    _REGISTRATION_SERVICE_URL = "https://agrirouter-registration-service-hubqa-eu10.cfapps.eu10.hana.ondemand.com"

    AR_PUBLIC_KEY = AR_QA_PUBLIC_KEY
