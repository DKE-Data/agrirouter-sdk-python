import base64
import json
from typing import Union


class AuthResponse:
    SIGNATURE_KEY = "signature"
    STATE_KEY = "state"
    TOKEN_KEY = "token"
    ERROR_KEY = "error"

    CRED_KEY = "credentials"

    def __init__(self, query_params):
        self._state = query_params.get(self.STATE_KEY, None)
        self._signature = query_params.get(self.SIGNATURE_KEY, None)
        self._token = query_params.get(self.TOKEN_KEY, None)
        self._error = query_params.get(self.ERROR_KEY, None)
        self.is_successful = not bool(self._error)
        self.is_valid = False

    def verify(self) -> None:
        """
        Validates signature according to docs:
        https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/integration/authorization.html#analyse-result

        If signature is not valid, all actions with AuthResponse instance
         will fail with BadAuthResponse

        :return:
        """
        # TODO: implement validation of response according to docs:
        # https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/integration/authorization.html#analyse-result

        self.is_valid = True

    @staticmethod
    def decode_token(token: Union[str, bytes]) -> dict:
        if type(token) == str:
            token = token.encode("ASCII")
        base_64_decoded_token = base64.b64decode(token)
        decoded_token = base_64_decoded_token.decode("ASCII")
        return json.loads(decoded_token)

    def get_auth_result(self) -> dict:
        if not self.is_successful:
            return {self.ERROR_KEY: self._error}
        decoded_token = self.decode_token(self._token)
        return {
            self.SIGNATURE_KEY: self._signature,
            self.STATE_KEY: self._state,
            self.TOKEN_KEY: self._token,
            self.CRED_KEY: decoded_token
        }


def decorator(func):
    pass
