"""Test agrirouter/onboarding/request.py"""

from agrirouter import OnboardParameters, SecuredOnboardingService
from agrirouter.onboarding.enums import Gateways, CertificateTypes
from tests.common.constants import APPLICATION_ID, PUBLIC_KEY, PRIVATE_KEY, ENV


class TestBaseOnboardingRequest:
    reg_code = "8eloz190fd"
    content_type = "json"
    certification_version_id = "13"
    utc_timestamp = "+03:00"
    time_zone = "01-01-2021"
    url = "localhost"
    params = OnboardParameters(
        id_=1,
        application_id=APPLICATION_ID,
        content_type=content_type,
        certification_version_id=certification_version_id,
        gateway_id=Gateways.MQTT.value,
        certificate_type=CertificateTypes.PEM.value,
        utc_timestamp=utc_timestamp,
        time_zone=time_zone,
        reg_code=reg_code,
    )
    onboarding = SecuredOnboardingService(
        public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, env=ENV
    )
    test_object = onboarding._create_request(params)

    def test_get_data(self):
        assert self.test_object.get_data()["applicationId"] == APPLICATION_ID
        assert (
                self.test_object.get_data()["certificateType"] == CertificateTypes.PEM.value
        )
        assert (
                self.test_object.get_data()["certificateType"] == CertificateTypes.PEM.value
        )

    def test_get_header(self):
        assert (
                self.test_object.get_header()["Authorization"] == "Bearer " + self.reg_code
        )
        assert self.test_object.get_header()["Content-Type"] == self.content_type
        assert (
                self.test_object.get_header()["X-Agrirouter-ApplicationId"] == APPLICATION_ID
        )
