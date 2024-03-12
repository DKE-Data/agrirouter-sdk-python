import json
from typing import Union

from agrirouter.api.exceptions import WrongField


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
            self.HOST: self.host,
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
                raise WrongField(f"Unknown field {key} for Connection Criteria class")

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

    def __str__(self):
        return str(self.json_serialize())

    def __repr__(self):
        return str(self.json_serialize())


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
                raise WrongField(f"Unknown field {key} for Authentication class")

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

    def __str__(self):
        return str(self.json_serialize())

    def __repr__(self):
        return str(self.json_serialize())


class ErrorResponse:
    CODE = "code"
    MESSAGE = "message"
    TARGET = "target"
    DETAILS = "details"

    def __init__(self,
                 *,
                 code: str = None,
                 message: str = None,
                 target: str = None,
                 details: str = None
                 ):
        self.code = code
        self.message = message
        self.target = target
        self.details = details

    def json_serialize(self) -> dict:
        return {
            self.CODE: self.code,
            self.MESSAGE: self.message,
            self.TARGET: self.target,
            self.DETAILS: self.details
        }

    def json_deserialize(self, data: Union[str, dict]) -> None:
        data = data if type(data) == dict else json.loads(data)
        for key, value in data.items():
            if key == self.CODE:
                self.code = value
            elif key == self.MESSAGE:
                self.message = value
            elif key == self.TARGET:
                self.target = value
            elif key == self.DETAILS:
                self.details = value
            else:
                raise WrongField(f"Unknown field {key} for ErrorResponse class")

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
