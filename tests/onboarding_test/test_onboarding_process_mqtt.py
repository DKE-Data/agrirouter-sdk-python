import pytest

from agrirouter.onboarding.onboarding import OnboardingService
from agrirouter.environments.environments import QAEnvironment
from agrirouter.onboarding.enums import CertificateTypes, GateWays
from agrirouter.onboarding.parameters import OnboardParameters
from agrirouter.onboarding.response import OnboardResponse
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.data.identifier import Identifier


@pytest.fixture(scope='module')
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

    @pytest.mark.skip(reason="Will fail unless registration code is changed")
    def test_update_recipient_with_PEM(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_RECIPIENT['id'],
            _environment=self._environment,
            registration_code="78ddb81011",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT['Path'], onboard_response)


class TestSingleMqttEndpointWithP12Certificate:
    _environment = QAEnvironment()

    @pytest.mark.skip(reason="Will fail unless registration code is changed")
    def test_update_recipient_with_P12(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_RECIPIENT['id'],
            _environment=self._environment,
            registration_code="27e788781b",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT['Path'], onboard_response)


class TestSenderSingleMqttEndpointWithPEMCertificate:
    _environment = QAEnvironment()

    @pytest.mark.skip(reason="Will fail unless registration code is changed")
    def test_update_sender_with_PEM(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_SENDER['id'],
            _environment=self._environment,
            registration_code="8fb74f7c85",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER['Path'], onboard_response)


class TestSenderSingleMqttEndpointWithP12Certificate:
    _environment = QAEnvironment()

    @pytest.mark.skip(reason="Will fail unless registration code is changed")
    def test_update_sender_with_P12(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_SENDER['id'],
            _environment=self._environment,
            registration_code="1c14568c64",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER['Path'], onboard_response)
