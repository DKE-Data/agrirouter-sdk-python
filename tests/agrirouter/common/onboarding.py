from agrirouter.service.onboarding import OnboardingService
from agrirouter.service.onboarding import OnboardParameters
from agrirouter.service.onboarding import OnboardResponse
from tests.agrirouter.data.applications import CommunicationUnit


def onboard_communication_unit(uuid: str, _environment, registration_code: str,
                               certification_type_definition: str = "PEM",
                               gateway_id: str = "2") -> OnboardResponse:
    """
    Onboard a single endpoint (Communication Unit) and return the onboard response.
     """
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
