import logging
import unittest

from agrirouter import CapabilitiesService, CapabilitiesParameters, OnboardingService, OnboardParameters
from agrirouter.environments.environments import QAEnvironment
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.messaging.enums import CapabilityType, CapabilityDirectionType
from agrirouter.messaging.services.commons import HttpMessagingService
from agrirouter.messaging.services.http.fetch_message_service import FetchMessageService
from agrirouter.onboarding.response import OnboardResponse
from agrirouter.utils.uuid_util import new_uuid
from applications import CommunicationUnit
from onboard_response_integration_service import save_onboard_response
from tests.common.sleeper import Sleeper
from tests.data.identifier import Identifier


class OnboardResponseUpdate(unittest.TestCase):
    _log = logging.getLogger(__name__)
    _environment = QAEnvironment()

    def test_update_http_cu_recipient(self):
        onboard_response = self._onboard(Identifier.HTTP_RECIPIENT_PEM['id'], "97b9851e9b")
        save_onboard_response(Identifier.HTTP_RECIPIENT_PEM['path'], onboard_response)
        self._validate_connection(onboard_response)
        self._enable_all_capabilities_via_http(onboard_response)

    def test_update_http_cu_sender(self):
        onboard_response = self._onboard(Identifier.HTTP_SENDER_PEM['id'], "39220f2ce0")
        save_onboard_response(Identifier.HTTP_SENDER_PEM['path'], onboard_response)
        self._validate_connection(onboard_response)
        self._enable_all_capabilities_via_http(onboard_response)

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
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_DEVICE_DESCRIPTION.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.ISO_11783_TIMELOG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_BMP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_JPEG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.IMG_PNG.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.SHP_SHAPE_ZIP.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.DOC_PDF.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.VID_AVI.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.VID_MP4.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.VID_WMV.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_parameters.capability_parameters.append(
            CapabilitySpecification.Capability(technical_message_type=CapabilityType.GPS_INFO.value,
                                               direction=CapabilityDirectionType.SEND_RECEIVE.value))
        capabilities_service.send(capabilities_parameters)
        Sleeper.process_the_command()
        fetch_message_service = FetchMessageService()
        fetch = fetch_message_service.fetch(onboard_response).get_messages()
        assert len(fetch) == 1
