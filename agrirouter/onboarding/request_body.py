import json
from datetime import datetime

from agrirouter.onboarding.enums import CertificateTypes, GateWays
from agrirouter.onboarding.exceptions import WrongCertificationType, WrongGateWay


class SoftwareOnboardingBody:
    def __init__(self,
                 *,
                 id_,
                 application_id,
                 certification_version_id,
                 gateway_id,
                 certificate_type,
                 time_zone=None,
                 utc_timestamp=None
                 ):

        self._validate_certificate_type(certificate_type)
        self._validate_gateway_id(gateway_id)

        #utc_timestamp = utc_timestamp if utc_timestamp else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        self._set_params(
            id_,
            application_id,
            certification_version_id,
            gateway_id,
            certificate_type,
            #utc_timestamp,
            #time_zone
        )

    def get_parameters(self) -> dict:
        return self.params

    def _set_params(self,
                    id_,
                    application_id,
                    certification_version_id,
                    gateway_id,
                    certificate_type,
                    utc_timestamp=None,
                    time_zone=None
                    ):

        self.params = {
            "id": id_,
            "applicationId": application_id,
            "certificationVersionId": certification_version_id,
            "gatewayId": gateway_id,
            "certificateType": certificate_type,
            #"UTCTimestamp": utc_timestamp,
            #"timeZone": time_zone,
        }

    def json(self) -> str:
        return json.dumps(self.get_parameters(), separators=(',', ':'))

    @staticmethod
    def _validate_certificate_type(certificate_type: str) -> None:
        if certificate_type not in CertificateTypes.values_list():
            raise WrongCertificationType

    @staticmethod
    def _validate_gateway_id(gateway_id: str) -> None:
        if gateway_id not in GateWays.values_list():
            raise WrongGateWay
