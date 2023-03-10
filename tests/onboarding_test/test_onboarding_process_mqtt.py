import pytest

from agrirouter.onboarding.onboarding import OnboardingService
from agrirouter.environments.environments import QAEnvironment
from agrirouter.onboarding.enums import CertificateTypes, GateWays
from agrirouter.onboarding.parameters import OnboardParameters
from agrirouter.onboarding.response import OnboardResponse
from tests.data import identifier
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.constants import cu_recipient_endpoint_id


@pytest.fixture
def onboarding_process_fixture():
    def __onboard(uuid: str, _environment, registration_code: str, certification_type_definition: str = "PEM",
                  gateway_id: str = "2") -> OnboardResponse:
        onboarding_service = OnboardingService(env=_environment)
        onboarding_parameters = OnboardParameters(
            id_=uuid,
            reg_code=registration_code,
            certificate_type=certification_type_definition,
            gateway_id=gateway_id,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            time_zone="+01:00"
        )

        onboard_response = onboarding_service.onboard(onboarding_parameters)
        assert onboard_response.device_alternate_id != ''
        assert onboard_response.sensor_alternate_id != ''
        assert onboard_response.capability_alternate_id != ''
        assert onboard_response.authentication.certificate != ''
        assert onboard_response.authentication.secret != ''
        assert onboard_response.authentication.type != ''
        assert onboard_response.connection_criteria.commands != ''
        assert onboard_response.connection_criteria.measures != ''

        return onboard_response

    return __onboard


class TestSingleMqttEndpointWithPEMCertificate:
    _environment = QAEnvironment()

    def test_update_recipient_with_PEM(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=cu_recipient_endpoint_id,
            _environment=self._environment,
            registration_code="032ecf9480",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        # self._enable_all_capabilities_via_mqtt(onboard_response)
        OnboardResponseIntegrationService.save(identifier.MQTT_RECIPIENT, onboard_response)


class TestSingleMqttEndpointWithP12Certificate:
    _environment = QAEnvironment()

    def test_update_recipient_with_P12(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=cu_recipient_endpoint_id,
            _environment=self._environment,
            registration_code="74cb298919",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        # self._enable_all_capabilities_via_mqtt(onboard_response)
        OnboardResponseIntegrationService.save(identifier.MQTT_RECIPIENT, onboard_response)
