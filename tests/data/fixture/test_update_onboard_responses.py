import pytest

from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.onboarding.onboarding import SecuredOnboardingService, OnboardingService
from agrirouter.onboarding.parameters import OnboardParameters
from agrirouter.messaging.services.messaging import SubscriptionService, CapabilitiesService, FeedConfirmService, \
    FeedDeleteService, QueryHeaderService, QueryMessagesService, ListEndpointsService
from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters, \
    QueryMessageParameters, QueryHeaderParameters, CloudOffboardParameters, CloudOnboardParameters, \
    CapabilitiesParameters, FeedConfirmParameters, FeedDeleteParameters, ListEndpointsParameters, MessageParameters, \
    SubscriptionParameters
from agrirouter.environments.environments import QAEnvironment
from agrirouter.messaging.services.commons import HttpMessagingService
from agrirouter.messaging.services.http.fetch_message_service import FetchMessageService
from agrirouter.onboarding.onboarding import OnboardingService
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.uuid_util import new_uuid
from tests.data import identifier
from tests.data.applications import CommunicationUnit
from tests.data.onboard_response_integration_service import OnboardResponseIntegrationService
from tests.constants import cu_recipient_endpoint_id


class TestUpdateOnboardResponses:
    _environment = QAEnvironment()

    def test_update_recipient(self):
        onboard_response = self._onboard(cu_recipient_endpoint_id, "ed1e44c97c")
        self._validate_connection(onboard_response)
        self._enable_all_capabilities_via_http(onboard_response)
        OnboardResponseIntegrationService.save(identifier.RECIPIENT, onboard_response)

    def _onboard(self, uuid: str, registration_code: str, certification_type_definition: str = "PEM",
                 gateway_id: str = "3") -> OnboardResponse:
        onboarding_service = OnboardingService(env=self._environment)
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

    def _validate_connection(self, onboard_response: OnboardResponse):
        fetch_message_service = FetchMessageService()
        fetch = fetch_message_service.fetch(onboard_response).get_messages()
        assert len(fetch) == 0

    def _enable_all_capabilities_via_http(self, onboard_response: OnboardResponse):
        messaging_service = HttpMessagingService()
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=new_uuid(),
            application_message_seq_no=1,
            application_id=CommunicationUnit.application_id,
            certification_version_id=CommunicationUnit.certification_version_id,
            enable_push_notification=CapabilitySpecification.PushNotification.DISABLED,
            capability_parameters=[]
        )
        # TODO: continue here, capability helper with All Capabilities should be implemented next
        # capabilities_parameters.capability_parameters.append()
