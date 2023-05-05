import pytest

from agrirouter.environments.environments import QAEnvironment
from agrirouter.onboarding.enums import CertificateTypes, Gateways
from tests.common.onboarding import onboard_communication_unit
from tests.data.identifier import Identifier
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService


class TestSingleMqttEndpointWithPEMCertificate:

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient_with_pem(self):
        """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_RECIPIENT_PEM[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="efd9b2fbaa",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT_PEM[Identifier.PATH], onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_recipient_with_p12(self):
        """ Test the onboarding process for a single MQTT endpoint with a P12 certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_RECIPIENT_P12[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="d8d256c752",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_RECIPIENT_P12[Identifier.PATH], onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_sender_with_pem(self):
        """ Test the onboarding process for a single MQTT endpoint with a PEM certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_SENDER_PEM[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="ef0f89246d",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER_PEM[Identifier.PATH], onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_sender_with_p12(self):
        """ Test the onboarding process for a single MQTT endpoint with a P12 certificate. """
        onboard_response = onboard_communication_unit(
            uuid=Identifier.MQTT_SENDER_P12[Identifier.ID],
            _environment=QAEnvironment(),
            registration_code="61124dd64b",
            certification_type_definition=str(CertificateTypes.P12.value),
            gateway_id=str(Gateways.MQTT.value)
        )

        OnboardResponseIntegrationService.save(Identifier.MQTT_SENDER_P12[Identifier.PATH], onboard_response)
