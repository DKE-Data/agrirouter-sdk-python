from urllib.parse import urlparse, parse_qs

from agrirouter.api.env import EnvironmentalService
from agrirouter.service.dto.response.authorization import AuthResponse
from agrirouter.service.parameter.authorization import AuthUrlParameter


class AuthorizationService(EnvironmentalService):
    SIGNATURE_KEY = "signature"
    STATE_KEY = "state"
    TOKEN_KEY = "token"
    ERROR_KEY = "error"

    def __init__(self, env, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key
        super(AuthorizationService, self).__init__(env)

    def get_auth_request_url(self, parameters: AuthUrlParameter) -> str:
        auth_parameters = parameters.get_parameters()
        return self._environment.get_secured_onboarding_authorization_url(**auth_parameters)

    def extract_auth_response(self, url: str) -> AuthResponse:
        parsed_url = urlparse(url)
        query_params = self._extract_query_params(parsed_url.query)
        return AuthResponse(query_params)

    def verify_auth_response(self, response, public_key=None):
        public_key = public_key if public_key else self._environment.get_env_public_key()
        response.verify(public_key)

    @staticmethod
    def _extract_query_params(query_params: str) -> dict:
        qp_pairs = parse_qs(query_params)
        return {k: v[0] for k, v in qp_pairs.items()}
