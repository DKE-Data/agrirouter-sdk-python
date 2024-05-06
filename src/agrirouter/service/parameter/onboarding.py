from agrirouter.api.enums import CertificateTypes
from agrirouter.api.enums import ContentTypes
from agrirouter.util.utc_time_util import UtcTimeUtil


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
                 certificate_type: object = CertificateTypes.PEM.value,
                 ):
        self.id_ = id_
        self.application_id = application_id
        self.certification_version_id = certification_version_id
        self.gateway_id = str(gateway_id)
        self.certificate_type = certificate_type
        self.utc_timestamp = str(utc_timestamp) if utc_timestamp else UtcTimeUtil.now_as_utc_str()
        self.time_zone = str(time_zone)
        self.reg_code = reg_code

    def get_header_params(self):
        return {
            "content_type": ContentTypes.APPLICATION_JSON.value,
            "reg_code": self.reg_code,
            "application_id": self.application_id,
        }

    def get_body_params(self):
        return {
            "id_": self.id_,
            "application_id": self.application_id,
            "certification_version_id": self.certification_version_id,
            "gateway_id": self.gateway_id,
            "certificate_type": self.certificate_type,
            "utc_timestamp": self.utc_timestamp,
            "time_zone": self.time_zone,
        }
