import base64
import json
from typing import Union
from urllib.parse import unquote

from cryptography.exceptions import InvalidSignature

from agrirouter.service.dto.request.authorization import AuthorizationToken, AuthorizationResultUrl
from agrirouter.service.signature import SignatureService


class AuthResponse:
    SIGNATURE_KEY = "signature"
    STATE_KEY = "state"
    TOKEN_KEY = "token"
    ERROR_KEY = "error"

    CRED_KEY = "credentials"

    def __init__(self, query_params):
        self.state = query_params.get(self.STATE_KEY, None)
        self.signature = query_params.get(self.SIGNATURE_KEY, None)
        self.token = query_params.get(self.TOKEN_KEY, None)
        self.error = query_params.get(self.ERROR_KEY, None)
        self.is_successful = not bool(self.error)
        self._was_verified = False
        self._is_valid = False

    @property
    def is_valid(self):
        if not self._was_verified:
            raise PermissionError("The response was not verified yet. Please verify first. "
                                  "You can access is_valid only after verifying")

        return self._is_valid

    def verify(self, public_key) -> None:
        """
        Validates signature according to docs:
        https://docs.my-agrirouter.com/agrirouter-interface-documentation/latest/integration/authorization.html#analyse-result
            #
        If signature is not valid, all actions with AuthResponse instance
        will fail with BadAuthResponse
            #
        :return:
        """

        encoded_data = self.state + self.token
        unquoted_signature = unquote(self.signature)
        encoded_signature = base64.b64decode(unquoted_signature.encode("utf-8"))

        self._is_valid = True
        try:
            SignatureService.verify_signature(encoded_data, encoded_signature, public_key)
        except InvalidSignature:
            print("Response is invalid: invalid signature.")
            self._is_valid = False
        finally:
            self._was_verified = True

    @staticmethod
    def decode_token(token: Union[str, bytes]) -> AuthorizationToken:
        if type(token) == str:
            token = token.encode("utf-8")
        base_64_decoded_token = base64.b64decode(token)
        decoded_token = base_64_decoded_token.decode("utf-8")

        auth_token = AuthorizationToken()
        auth_token.json_deserialize(json.loads(decoded_token))
        return auth_token

    def get_auth_result(self) -> AuthorizationResultUrl:
        decoded_token = self.decode_token(self.token)

        return AuthorizationResultUrl(
            signature=self.signature,
            state=self.state,
            token=self.token,
            decoded_token=decoded_token,
            error=self.error
        )

    def get_signature(self):
        return self.signature

    def set_signature(self, signature):
        self.signature = signature

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
