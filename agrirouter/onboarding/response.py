from requests import Response

from agrirouter.onboarding.dto import ErrorResponse, ConnectionCriteria, Authentication


class BaseOnboardingResonse:

    def __init__(self, http_response: Response):
        response_body = http_response.json()

        self._status_code = http_response.status_code
        self._text = http_response.text

        self.connection_criteria = ConnectionCriteria(
            gateway_id=response_body.get("connectionCriteria").get("gatewayId"),
            measures=response_body.get("connectionCriteria").get("measures"),
            commands=response_body.get("connectionCriteria").get("commands"),
            host=response_body.get("connectionCriteria").get("host"),
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

    def get_authentication(self) -> Authentication:
        return self.authentication

    def get_sensor_alternate_id(self) -> str:
        return self.sensor_alternate_id

    def get_device_alternate_id(self) -> str:
        return self.device_alternate_id

    def get_capability_alternate_id(self) -> str:
        return self.capability_alternate_id

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
    pass


class SoftwareOnboardingResponse(BaseOnboardingResonse):
    """
    Response from onboarding request used for Farming Software or Telemetry Platform
    """

    def get_connection_criteria(self) -> dict:
        response_data = self.data()
        return response_data.get("connectionCriteria")

    def get_sensor_alternate_id(self):
        response_data = self.data()
        return response_data.get("sensorAlternateId")

    def get_authentication(self):
        response_data = self.data()
        return response_data.get("authentication")


class CUOnboardingResponse(BaseOnboardingResonse):
    """
    Response from onboarding request used for CUs
    """
    pass

