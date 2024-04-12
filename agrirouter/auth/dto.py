import json
from typing import Union

from agrirouter.api.exceptions import WrongField


class AuthorizationToken:
    ACCOUNT = 'account'
    REGISTRATION_CODE = 'regcode'
    EXPIRES = 'expires'

    def __init__(self,
                 *,
                 account: str = None,
                 regcode: str = None,
                 expires: str = None
                 ):
        self.account = account
        self.regcode = regcode
        self.expires = expires

    def json_deserialize(self, data: Union[str, dict]) -> None:
        data = data if type(data) == dict else json.loads(data)
        for key, value in data.items():
            if key == self.ACCOUNT:
                self.account = value
            elif key == self.REGISTRATION_CODE:
                self.regcode = value
            elif key == self.EXPIRES:
                self.expires = value
            else:
                raise WrongField(f"Unknown field {key} for AuthorizationToken class")

    def get_account(self) -> str:
        return self.account

    def set_account(self, account: str) -> None:
        self.account = account

    def get_regcode(self) -> str:
        return self.regcode

    def set_regcode(self, regcode: str) -> None:
        self.regcode = regcode

    def get_expires(self) -> str:
        return self.expires

    def set_expires(self, expires: str) -> None:
        self.expires = expires


class AuthorizationResultUrl:
    def __init__(self,
                 *,
                 state: str = None,
                 signature: str = None,
                 token: str = None,
                 decoded_token: AuthorizationToken = None,
                 error: str = None
                 ):
        self.state = state
        self.signature = signature
        self.token = token
        self.decoded_token = decoded_token
        self.error = error

    def get_state(self) -> str:
        return self.state

    def set_state(self, state: str) -> None:
        self.state = state

    def get_signature(self) -> str:
        return self.signature

    def set_signature(self, signature: str) -> None:
        self.signature = signature

    def get_token(self) -> str:
        return self.token

    def set_token(self, token: str) -> None:
        self.token = token

    def get_error(self) -> str:
        return self.error

    def set_error(self, error: str) -> None:
        self.error = error

    def get_decoded_token(self) -> AuthorizationToken:
        return self.decoded_token

    def set_decoded_token(self, decoded_token: AuthorizationToken) -> None:
        self.decoded_token = decoded_token


class AuthorizationResult:
    def __init__(self,
                 *,
                 authorization_url: str = None,
                 state: str = None,
                 ):
        self.authorization_url = authorization_url
        self.state = state

    def get_authorization_url(self) -> str:
        return self.authorization_url

    def set_authorization_url(self, authorization_url: str) -> None:
        self.authorization_url = authorization_url

    def get_state(self) -> str:
        return self.state

    def set_state(self, state: str) -> None:
        self.state = state
