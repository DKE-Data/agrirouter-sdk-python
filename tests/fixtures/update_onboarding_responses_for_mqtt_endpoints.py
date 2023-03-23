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
    """ Fixture for the onboarding process. """

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
    """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient_with_pem(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_RECIPIENT_PEM[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="efd9b2fbaa",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH], onboard_response)


class TestSingleMqttEndpointWithP12Certificate:
    """ Test the onboarding process for a single MQTT endpoint with a P12 certificate. """

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient_with_p12(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_RECIPIENT_P12[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="d8d256c752",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT_P12[Identifier.PATH], onboard_response)


class TestSenderSingleMqttEndpointWithPEMCertificate:
    """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_sender_with_pem(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_SENDER_PEM[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="ef0f89246d",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER_PEM[Identifier.PATH], onboard_response)


class TestSenderSingleMqttEndpointWithP12Certificate:
    """ Test the onboarding process for a single MQTT endpoint with a P12 certificate. """

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_sender_with_p12(self, onboarding_process_fixture):
        onboard_response = onboarding_process_fixture(
            uuid=Identifier.MQTT_SENDER_P12[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="61124dd64b",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(GateWays.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER_P12[Identifier.PATH], onboard_response)
