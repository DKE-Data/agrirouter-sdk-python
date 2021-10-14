import json
from typing import Union

from agrirouter.messaging.exceptions import WrongFieldError


class ConnectionCriteria:
    CLIENT_ID = 'clientId'
    COMMANDS = 'commands'
    GATEWAY_ID = 'gatewayId'
    HOST = 'host'
    MEASURES = 'measures'
    PORT = 'port'

    def __init__(self,
                 *,
                 gateway_id: str = None,
                 measures: str = None,
                 commands: str = None,
                 host: str = None,
                 port: str = None,
                 client_id: str = None
                 ):
        self.gateway_id = gateway_id
        self.measures = measures
        self.commands = commands
        self.host = host
        self.port = port
        self.client_id = client_id

    def json_serialize(self) -> dict:
        return {
            self.GATEWAY_ID: self.gateway_id,
            self.MEASURES: self.measures,
            self.COMMANDS: self.commands,
            self.PORT: self.port,
            self.CLIENT_ID: self.client_id
        }

    def json_deserialize(self, data: Union[str, dict]) -> None:
        data = data if type(data) == dict else json.loads(data)
        for key, value in data.items():
            if key == self.GATEWAY_ID:
                self.gateway_id = value
            elif key == self.MEASURES:
                self.measures = value
            elif key == self.COMMANDS:
                self.commands = value
            elif key == self.HOST:
                self.host = value
            elif key == self.PORT:
                self.port = value
            elif key == self.CLIENT_ID:
                self.client_id = value
            else:
                raise WrongFieldError(f"Unknown field {key} for Connection Criteria class")

    def get_gateway_id(self) -> str:
        return self.gateway_id

    def set_gateway_id(self, gateway_id: str) -> None:
        self.gateway_id = gateway_id

    def get_measures(self) -> str:
        return self.measures

    def set_measures(self, measures: str) -> None:
        self.measures = measures

    def get_commands(self) -> str:
        return self.commands

    def set_commands(self, commands: str) -> None:
        self.commands = commands

    def get_host(self) -> str:
        return self.host

    def set_host(self, host: str) -> None:
        self.host = host

    def get_port(self) -> str:
        return self.port

    def set_port(self, port: str) -> None:
        self.port = port

    def get_client_id(self) -> str:
        return self.client_id

    def set_client_id(self, client_id: str) -> None:
        self.client_id = client_id


class Authentication:
    TYPE = 'type'
    SECRET = 'secret'
    CERTIFICATE = 'certificate'

    def __init__(self,
                 *,
                 type: str = None,
                 secret: str = None,
                 certificate: str = None,
                 ):
        self.type = type
        self.secret = secret
        self.certificate = certificate

    def json_serialize(self) -> dict:
        return {
            self.TYPE: self.type,
            self.SECRET: self.secret,
            self.CERTIFICATE: self.certificate,
        }

    def json_deserialize(self, data: Union[str, dict]) -> None:
        data = data if type(data) == dict else json.loads(data)
        for key, value in data.items():
            if key == self.TYPE:
                self.type = value
            elif key == self.SECRET:
                self.secret = value
            elif key == self.CERTIFICATE:
                self.certificate = value
            else:
                raise WrongFieldError(f"Unknown field {key} for Authentication class")

    def get_type(self) -> str:
        return self.type

    def set_type(self, type: str) -> None:
        self.type = type

    def get_secret(self) -> str:
        return self.secret

    def set_secret(self, secret: str) -> None:
        self.secret = secret

    def get_certificate(self) -> str:
        return self.certificate

    def set_certificate(self, certificate: str) -> None:
        self.certificate = certificate


class AuthorizationResultUrl:
    def __init__(self,
                 *,
                 state: str = None,
                 signature: str = None,
                 token: str = None,
                 error: str = None
                 ):
        self.state = state
        self.signature = signature
        self.token = token
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
                raise WrongFieldError(f"Unknown field {key} for AuthorizationToken class")

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


class ErrorResponse:
    def __init__(self,
                 *,
                 code,
                 message,
                 target,
                 details
                 ):
        self.code = code
        self.message = message
        self.target = target
        self.details = details

    def get_code(self) -> str:
        return self.code

    def set_code(self, code: str) -> None:
        self.code = code

    def get_message(self) -> str:
        return self.message

    def set_message(self, message: str) -> None:
        self.message = message

    def get_target(self) -> str:
        return self.target

    def set_target(self, target: str) -> None:
        self.target = target

    def get_details(self) -> str:
        return self.details

    def set_details(self, details: str) -> None:
        self.details = details
