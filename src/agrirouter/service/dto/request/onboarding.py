import json
import logging
from datetime import datetime

from agrirouter.api.enums import RequestHeaders, CertificateTypes, Gateways, ContentTypes
from agrirouter.api.exceptions import WrongCertificationType, WrongGateWayType, MissingRegistrationCode
from agrirouter.service.parameter.onboarding import OnboardParameters
from agrirouter.service.signature import SignatureService


class SoftwareOnboardingHeader:
    def __init__(self,
                 reg_code: str,
                 application_id: str = None,
                 signature: str = None,
                 content_type=ContentTypes.APPLICATION_JSON.value
                 ):
        self._set_params(reg_code, content_type, application_id, signature)

    def get_header(self) -> dict:
        return self.params

    def sign(self, signature: str):
        self.params[RequestHeaders.X_AGRIROUTER_SIGNATURE.value] = signature

    def _set_params(self, reg_code: str, content_type: str, application_id: str, signature: str = None):
        header = dict()

        if reg_code:
            header[RequestHeaders.AUTHORIZATION.value] = f"Bearer {reg_code}"
        else:
            raise MissingRegistrationCode("Registration code is required")

        if content_type:
            header[RequestHeaders.CONTENT_TYPE.value] = content_type
        else:
            logging.warning("Content-Type not set, defaulting to application/json")
            header[RequestHeaders.CONTENT_TYPE.value] = ContentTypes.APPLICATION_JSON.value

        if application_id:
            header[RequestHeaders.X_AGRIROUTER_APPLICATION_ID.value] = application_id

        if signature:
            header[RequestHeaders.X_AGRIROUTER_SIGNATURE.value] = signature if signature else ""

        self.params = header


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

        utc_timestamp = utc_timestamp if utc_timestamp else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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
                    utc_timestamp=None,
                    time_zone=None
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

    def json(self) -> str:
        return json.dumps(self.get_parameters(), separators=(',', ':'))

    @staticmethod
    def _validate_certificate_type(certificate_type: str) -> None:
        if certificate_type not in CertificateTypes.values_list():
            raise WrongCertificationType

    @staticmethod
    def _validate_gateway_id(gateway_id: str) -> None:
        if gateway_id not in Gateways.values_list():
            raise WrongGateWayType


class OnboardRequest:
    def __init__(self, header: SoftwareOnboardingHeader, body: SoftwareOnboardingBody):
        self.header = header
        self.body = body

    @classmethod
    def from_onboard_parameters(cls, params: OnboardParameters) -> 'OnboardRequest':
        body_params = params.get_body_params()
        request_body = SoftwareOnboardingBody(**body_params)

        header_params = params.get_header_params()
        request_header = SoftwareOnboardingHeader(**header_params)

        return cls(header=request_header, body=request_body)

    def get_data(self):
        return self.body.get_parameters()

    def get_header(self):
        return self.header.get_header()

    def get_body_content(self):
        return self.body.json().replace("\n", "")

    def sign(self, private_key, public_key):
        body = self.get_body_content()
        signature = SignatureService.create_signature(body, private_key)
        SignatureService.verify_signature(body, bytes.fromhex(signature), public_key)
        self.header.sign(signature)

    @property
    def is_signed(self):
        header_has_signature = self.get_header().get(RequestHeaders.X_AGRIROUTER_SIGNATURE.value, None)
        if header_has_signature:
            return True
        return False
