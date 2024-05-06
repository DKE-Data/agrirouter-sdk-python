from agrirouter.api.constants import AR_QA_PUBLIC_KEY, AR_PROD_PUBLIC_KEY


class BaseEnvironment:
    _LOGIN_URL = "/app"
    _MQTT_URL_TEMPLATE = "ssl://{host}:{port}"
    _SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE = \
        "/application/{application_id}/authorize" \
        "?response_type={response_type}&state={state}"
    _ENV_BASE_URL = ""
    _API_PREFIX = ""
    _REGISTRATION_SERVICE_URL = ""
    _AR_PUBLIC_KEY = None

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
        return self.get_base_url() + self._LOGIN_URL

    def get_secured_onboarding_authorization_url(self, application_id, response_type, state, redirect_uri=None) -> str:
        auth_url = self.get_base_url() + self._SECURED_ONBOARDING_AUTHORIZATION_LINK_TEMPLATE.format(
            application_id=application_id,
            response_type=response_type,
            state=state
        )
        return auth_url + f"&redirect_uri={redirect_uri}" if redirect_uri is not None else auth_url

    def get_mqtt_server_url(self, host, port) -> str:
        return self._MQTT_URL_TEMPLATE.format(host=host, port=port)

    def get_env_public_key(self):
        return self._AR_PUBLIC_KEY


class Production(BaseEnvironment):
    _ENV_BASE_URL = "https://goto.my-agrirouter.com"
    _API_PREFIX = "/api/v1.0"
    _REGISTRATION_SERVICE_URL = "https://onboard.my-agrirouter.com"
    _AR_PUBLIC_KEY = AR_PROD_PUBLIC_KEY


class Qa(BaseEnvironment):
    _ENV_BASE_URL = "https://agrirouter-qa.cfapps.eu10.hana.ondemand.com"
    _API_PREFIX = "/api/v1.0"
    _REGISTRATION_SERVICE_URL = "https://agrirouter-registration-service-hubqa-eu10.cfapps.eu10.hana.ondemand.com"
    _AR_PUBLIC_KEY = AR_QA_PUBLIC_KEY


class EnvironmentalService:
    """
    A class that provides environmental messaging based on the provided environment value.

    Attributes:
    - _environment (Environment): The current environment.
    """

    def __init__(self, env: BaseEnvironment):
        self._set_env(env)

    def _set_env(self, env) -> None:
        """
        Sets the environment based on the provided value.

        Parameters:
        - env (str): The desired environment value. Must be one of the following: `qa` or `production`.

        Raises:
        - InvalidEnvironmentSetup: If the provided environment value is not valid.
        """
        self._environment = env
