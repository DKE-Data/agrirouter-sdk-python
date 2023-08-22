"""Test agrirouter/onboarding/onboarding.py"""

import pytest

from agrirouter.onboarding.enums import Gateways, CertificateTypes
from agrirouter.onboarding.exceptions import WrongCertificationType, WrongGateWayType
from agrirouter.onboarding.onboarding import SecuredOnboardingService
from agrirouter.onboarding.parameters import OnboardParameters
from tests.common.constants import PUBLIC_KEY, PRIVATE_KEY, ENV, APPLICATION_ID


class TestSoftwareOnboarding:
    def test__create_request(self):
        params = OnboardParameters(
            id_=1,
            application_id=APPLICATION_ID,
            content_type="json",
            certification_version_id="13",
            gateway_id=Gateways.MQTT.value,
            certificate_type=CertificateTypes.PEM.value,
            utc_timestamp="+03:00",
            time_zone="01-01-2021",
            reg_code="8eloz190fd",
        )
        onboarding = SecuredOnboardingService(
            public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, env=ENV
        )
        assert onboarding._create_request(params)

        params = OnboardParameters(
            id_=2,
            application_id=APPLICATION_ID,
            content_type="json",
            certification_version_id="13",
            gateway_id=Gateways.MQTT.value,
            certificate_type="wrong_certificate",
            utc_timestamp="+03:00",
            time_zone="01-01-2021",
            reg_code="8eloz190fd",
        )
        onboarding = SecuredOnboardingService(
            public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, env=ENV
        )
        with pytest.raises(WrongCertificationType):
            assert onboarding._create_request(params)

        params = OnboardParameters(
            id_=3,
            application_id=APPLICATION_ID,
            content_type="content_type",
            certification_version_id="13",
            gateway_id="wrong_gateway_id",
            certificate_type=CertificateTypes.PEM.value,
            utc_timestamp="+03:00",
            time_zone="01-01-2021",
            reg_code="8eloz190fd",
        )
        onboarding = SecuredOnboardingService(
            public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, env=ENV
        )
        with pytest.raises(WrongGateWayType):
            assert onboarding._create_request(params)
