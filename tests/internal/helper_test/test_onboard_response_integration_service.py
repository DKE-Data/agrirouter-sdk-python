from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService


def test_onboard_response_integration_service():
    onboard_response = OnboardResponseIntegrationService.read("test")
