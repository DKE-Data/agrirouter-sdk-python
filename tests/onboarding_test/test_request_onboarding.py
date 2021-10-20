"""Test agrirouter/onboarding/request.py"""

from agrirouter import SoftwareOnboardingParameter, SoftwareOnboarding
from agrirouter.onboarding.enums import GateWays, CertificateTypes
from tests.constants import application_id, public_key, private_key, ENV


class TestBaseOnboardingRequest:
    reg_code = "8eloz190fd"
    content_type = "json"
    certification_version_id = "13"
    utc_timestamp = "+03:00"
    time_zone = "01-01-2021"
    url = "localhost"
    params = SoftwareOnboardingParameter(
        id_=1,
        application_id=application_id,
        content_type=content_type,
        certification_version_id=certification_version_id,
        gateway_id=GateWays.MQTT.value,
        certificate_type=CertificateTypes.PEM.value,
        utc_timestamp=utc_timestamp,
        time_zone=time_zone,
        reg_code=reg_code,
    )
    onboarding = SoftwareOnboarding(
        public_key=public_key, private_key=private_key, env=ENV
    )
    test_object = onboarding._create_request(params, url)

    def test_get_url(self):
        assert self.test_object.get_url() == self.url

    def test_get_data(self):
        assert self.test_object.get_data()["applicationId"] == application_id
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
            self.test_object.get_header()["X-Agrirouter-ApplicationId"]
            == application_id
        )
