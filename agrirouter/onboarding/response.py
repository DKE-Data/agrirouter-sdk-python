import json
from typing import Union

from requests import Response

from agrirouter.messaging.exceptions import WrongFieldError
from agrirouter.onboarding.dto import ErrorResponse, ConnectionCriteria, Authentication


class BaseOnboardingResonse:

    def __init__(self, http_response: Response):

        self._status_code = http_response.status_code
        self._text = http_response.text

    @property
    def status_code(self):
        return self._status_code

    @property
    def text(self):
        return self._text


class SoftwareVerifyOnboardingResponse(BaseOnboardingResonse):
    """
    Response from verify request used for Farming Software or Telemetry Platform before onboarding
    """

    def __init__(self, http_response: Response = None):
        if http_response:
            super(SoftwareVerifyOnboardingResponse, self).__init__(http_response)
            response_body = http_response.json()
        else:
            self._text = None
            self._status_code = None
            response_body = {}

        self.account_id = response_body.get("accountId", None)

        self.error = ErrorResponse(
            code=response_body.get("error").get("code"),
            message=response_body.get("error").get("message"),
            target=response_body.get("error").get("target"),
            details=response_body.get("error").get("details"),
        ) if response_body.get("error", None) else None

    def get_account_id(self) -> str:
        return self.account_id

    def set_account_id(self, account_id: str):
        self.account_id = account_id


class SoftwareOnboardingResponse(BaseOnboardingResonse):
    """
    Response from onboarding request used for CU
    """

    DEVICE_ALTERNATE_ID = "deviceAlternateId"
    CAPABILITY_ALTERNATE_ID = "capabilityAlternateId"
    SENSOR_ALTERNATE_ID = "sensorAlternateId"
    CONNECTION_CRITERIA = "connectionCriteria"
    AUTHENTICATION = "authentication"
    ERROR = "error"

    def __init__(self, http_response: Response = None):
        if http_response != None:
            super(SoftwareOnboardingResponse, self).__init__(http_response)
            response_body = http_response.json()
        else:
            self._text = None
            self._status_code = None
            response_body = {}

        self.connection_criteria = ConnectionCriteria(
            gateway_id=response_body.get("connectionCriteria").get("gatewayId"),
            measures=response_body.get("connectionCriteria").get("measures"),
            commands=response_body.get("connectionCriteria").get("commands"),
            host=response_body.get("connectionCriteria").get("host"),
            port=response_body.get("connectionCriteria").get("port"),
            client_id=response_body.get("connectionCriteria").get("clientId")
        ) if response_body.get("connectionCriteria", None) else None

        self.authentication = Authentication(
            type=response_body.get("authentication").get("type"),
            secret=response_body.get("authentication").get("secret"),
            certificate=response_body.get("authentication").get("certificate")
        ) if response_body.get("authentication", None) else None

        self.capability_alternate_id = response_body.get("capabilityAlternateId", None)
        self.device_alternate_id = response_body.get("deviceAlternateId", None)
        self.sensor_alternate_id = response_body.get("sensorAlternateId", None)

        self.error = ErrorResponse(
            code=response_body.get("error").get("code"),
            message=response_body.get("error").get("message"),
            target=response_body.get("error").get("target"),
            details=response_body.get("error").get("details"),
        ) if response_body.get("error", None) else None

    def get_connection_criteria(self) -> ConnectionCriteria:
        return self.connection_criteria

    def set_connection_criteria(self, connection_criteria: ConnectionCriteria):
        self.connection_criteria = connection_criteria

    def get_authentication(self) -> Authentication:
        return self.authentication

    def set_authentication(self, authentication: Authentication):
        self.authentication = authentication

    def get_sensor_alternate_id(self) -> str:
        return self.sensor_alternate_id

    def set_sensor_alternate_id(self, sensor_alternate_id: str):
        self.sensor_alternate_id = sensor_alternate_id

    def get_device_alternate_id(self) -> str:
        return self.device_alternate_id

    def set_device_alternate_id(self, device_alternate_id: str):
        self.device_alternate_id = device_alternate_id

    def get_capability_alternate_id(self) -> str:
        return self.capability_alternate_id

    def set_capability_alternate_id(self, capability_alternate_id: str):
        self.capability_alternate_id = capability_alternate_id

    def json_serialize(self):
        if self.error:
            return {
                self.ERROR: self.error
            }
        return {
            self.DEVICE_ALTERNATE_ID: self.device_alternate_id,
            self.CAPABILITY_ALTERNATE_ID: self.capability_alternate_id,
            self.SENSOR_ALTERNATE_ID: self.sensor_alternate_id,
            self.CONNECTION_CRITERIA: self.connection_criteria.json_serialize(),
            self.AUTHENTICATION: self.authentication.json_serialize()
        }

    def json_deserialize(self, data: Union[dict, str]):
        data_dict = data if type(data) == dict else json.loads(data)
        for (key, value) in data_dict.items():
            if key == self.DEVICE_ALTERNATE_ID:
                self.device_alternate_id = value
            elif key == self.CAPABILITY_ALTERNATE_ID:
                self.capability_alternate_id = value
            elif key == self.SENSOR_ALTERNATE_ID:
                self.sensor_alternate_id = value
            elif key == self.CONNECTION_CRITERIA:
                connection_criteria = ConnectionCriteria()
                connection_criteria.json_deserialize(value)
                self.connection_criteria = connection_criteria
            elif key == self.AUTHENTICATION:
                authentication = Authentication()
                authentication.json_deserialize(value)
                self.authentication = authentication
            elif key == self.ERROR:
                error_response = ErrorResponse()
                error_response.json_deserialize(value)
                self.error = error_response
            else:
                raise WrongFieldError(f"Unknown field `{key}` for {self.__class__}")

    def __str__(self):
        return str(self.json_serialize())

    def __repr__(self):
        return str(self.json_serialize())
