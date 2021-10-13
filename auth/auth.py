from urllib.parse import urlparse, parse_qs

from auth.exceptions import InvalidEnvironmentSetup
from auth.parameters import AuthUrlParameter
from auth.response import AuthResponse
from environments.environments import ProductionEnvironment, QAEnvironment


class Authorization:

    SIGNATURE_KEY = "signature"
    STATE_KEY = "state"
    TOKEN_KEY = "token"
    ERROR_KEY = "error"

    def __init__(self, env):
        self._set_env(env)

    def _set_env(self, env) -> None:
        if env == "QA":
            self._environment = QAEnvironment()
        elif env == "Production":
            self._environment = ProductionEnvironment()
        else:
            raise InvalidEnvironmentSetup(env=env)

    def get_auth_request_url(self, parameters: AuthUrlParameter) -> str:
        auth_parameters = parameters.get_parameters()
        return self._environment.get_secured_onboarding_authorization_url(**auth_parameters)

    def extract_auth_response(self, url: str) -> AuthResponse:
        parsed_url = urlparse(url)
        query_params = self._extract_query_params(parsed_url.query)
        return AuthResponse(query_params)

    def verify_auth_response(self):
        pass

    @staticmethod
    def _extract_query_params(query_params: str) -> dict:
        qp_pairs = parse_qs(query_params)
        return {k: v[0] for k, v in qp_pairs.items()}

