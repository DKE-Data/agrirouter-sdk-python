import json
from abc import ABC, abstractmethod

from onboarding.enums import CertificateTypes, GateWays
from onboarding.exceptions import WrongCertificationType, WrongGateWay


class BaseOnboardingBody(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_parameters(self, *args, **kwargs) -> dict:
        ...

    @abstractmethod
    def _set_params(self, *args, **kwargs):
        ...


class SoftwareOnboardingBody(BaseOnboardingBody):
    def __init__(self,
                 id_,
                 application_id,
                 certification_version_id,
                 gateway_id,
                 certificate_type,
                 utc_timestamp,
                 time_zone
                 ):

        self._validate_certificate_type(certificate_type)
        self._validate_gateway_id(gateway_id)

        self._set_params(
            id_,
            application_id,
            certification_version_id,
            gateway_id,
            certificate_type,
            utc_timestamp,
            time_zone
        )

    def get_parameters(self) -> dict:
        return self.params

    def _set_params(self,
                    id_,
                    application_id,
                    certification_version_id,
                    gateway_id,
                    certificate_type,
                    utc_timestamp,
                    time_zone
                    ):

        self.params = {
            "id": id_,
            "applicationId": application_id,
            "certificationVersionId": certification_version_id,
            "gatewayId": gateway_id,
            "certificateType": certificate_type,
            "UTCTimestamp": utc_timestamp,
            "timeZone": time_zone,
        }

    def json(self, new_lines: bool = True) -> str:
        result = json.dumps(self.get_parameters(), indent="")
        if not new_lines:
            return result.replace("\n", "")
        return result

    @staticmethod
    def _validate_certificate_type(certificate_type: str) -> None:
        if certificate_type not in CertificateTypes.values_list():
            raise WrongCertificationType

    @staticmethod
    def _validate_gateway_id(gateway_id: str) -> None:
        if gateway_id not in GateWays.values_list():
            raise WrongGateWay


class CUOnboardingBody(BaseOnboardingBody):

    def __init__(self, *args, **kwargs):
        ...

    def get_parameters(self, *args, **kwargs) -> dict:
        ...

    def _set_params(self, *args, **kwargs):
        ...

    def json(self, new_lines: bool = True) -> str:
        result = json.dumps(self.get_parameters(), indent="")
        if not new_lines:
            return result.replace("\n", "")
        return result
