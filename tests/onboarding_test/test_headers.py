"""Test agrirouter/onboarding/headers.py"""
from agrirouter.constants.media_types import ContentTypes
from agrirouter.onboarding.headers import SoftwareOnboardingHeader


class TestSoftwareOnboardingHeader:
    reg_code = "1AC2cs21W"
    test_object = SoftwareOnboardingHeader(reg_code=reg_code, application_id=1)
    test_object_1 = SoftwareOnboardingHeader(
        reg_code=reg_code, application_id=1, content_type="json"
    )

    def test_get_header(self):
        assert isinstance(self.test_object.get_header(), dict)
        assert (
            self.test_object.get_header()["Authorization"] == "Bearer " + self.reg_code
        )
        assert (
            self.test_object.get_header()["Content-Type"]
            == ContentTypes.APPLICATION_JSON.value
        )

        assert self.test_object_1.get_header()["Content-Type"] == "json"
