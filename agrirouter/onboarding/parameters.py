from agrirouter.constants.media_types import ContentTypes
from agrirouter.onboarding.enums import CertificateTypes


class OnboardParameters:
    def __init__(self,
                 *,
                 id_: object,
                 application_id: object,
                 certification_version_id: object,
                 gateway_id: object,
                 time_zone: object = None,
                 reg_code: object,
                 utc_timestamp: object = None,
                 content_type: object = ContentTypes.APPLICATION_JSON.value,
                 certificate_type: object = CertificateTypes.PEM.value,
                 ):
        self.id_ = id_
        self.application_id = application_id
        self.content_type = content_type
        self.certification_version_id = certification_version_id
        self.gateway_id = str(gateway_id)
        self.certificate_type = certificate_type
        # self.utc_timestamp = str(utc_timestamp) if utc_timestamp else now_as_utc_str()
        # self.time_zone = str(time_zone)
        self.reg_code = reg_code

    def get_header_params(self):
        return {
            "content_type": self.content_type,
            "reg_code": self.reg_code,
            # "application_id": self.application_id,
        }

    def get_body_params(self):
        return {
            "id_": self.id_,
            "application_id": self.application_id,
            "certification_version_id": self.certification_version_id,
            "gateway_id": self.gateway_id,
            "certificate_type": self.certificate_type,
            # "utc_timestamp": self.utc_timestamp,
            # "time_zone": self.time_zone,
        }
