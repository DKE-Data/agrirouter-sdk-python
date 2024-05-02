import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType, CapabilityDirectionType
from agrirouter.api.env import Qa
from agrirouter.generated.messaging.request.payload.endpoint.capabilities_pb2 import CapabilitySpecification
from agrirouter.service.parameter.messaging import CapabilitiesParameters
from agrirouter.service.messaging import HttpMessagingService
from agrirouter.service.messaging.http import FetchMessageService
from agrirouter.service.messaging import CapabilitiesService
from agrirouter.api.enums import CertificateTypes, Gateways
from agrirouter.service.onboarding import OnboardResponse
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.onboarding import onboard_communication_unit
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.applications import CommunicationUnit
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import save_onboard_response


class OnboardResponseUpdate(unittest.TestCase):
    _log = logging.getLogger(__name__)
    _environment = Qa()

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_http_cu_recipient(self):
        onboard_response = onboard_communication_unit(
            uuid=Identifier.HTTP_RECIPIENT_PEM[Identifier.ID],
            _environment=Qa(),
            registration_code="CHANGE_ME",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.HTTP.value)
        )
        save_onboard_response(Identifier.HTTP_RECIPIENT_PEM[Identifier.PATH], onboard_response)
        self._validate_connection(onboard_response)
        self._enable_all_capabilities_via_http(onboard_response)

    @pytest.mark.skip(reason="Will fail unless the registration code is changed")
    def test_update_http_cu_sender(self):
        onboard_response = onboard_communication_unit(
            uuid=Identifier.HTTP_SENDER_PEM[Identifier.ID],
            _environment=Qa(),
            registration_code="CHANGE_ME",
            certification_type_definition=str(CertificateTypes.PEM.value),
            gateway_id=str(Gateways.HTTP.value)
        )
        save_onboard_response(Identifier.HTTP_SENDER_PEM[Identifier.PATH], onboard_response)
        self._validate_connection(onboard_response)
        self._enable_all_capabilities_via_http(onboard_response)

    @staticmethod
    def _validate_connection(onboard_response: OnboardResponse):
        fetch_message_service = FetchMessageService()
        fetch = fetch_message_service.fetch(onboard_response).get_messages()
        assert len(fetch) == 0

    @staticmethod
    def _enable_all_capabilities_via_http(onboard_response: OnboardResponse):
        messaging_service = HttpMessagingService()
        capabilities_service = CapabilitiesService(messaging_service)
        capabilities_parameters = CapabilitiesParameters(
            onboarding_response=onboard_response,
            application_message_id=UUIDUtil.new_uuid(),
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
