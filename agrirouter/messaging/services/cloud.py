from agrirouter.generated.cloud_provider_integration.cloud_virtualized_app_registration_pb2 import OnboardingRequest, \
    OffboardingRequest
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope
from agrirouter.messaging.encode import encode_message
from agrirouter.messaging.enums import TechnicalMessageType
from agrirouter.messaging.messages import EncodedMessage
from agrirouter.messaging.parameters.service import MessageHeaderParameters, MessagePayloadParameters, \
    CloudOnboardParameters, CloudOffboardParameters
from agrirouter.messaging.services.messaging import AbstractService
from agrirouter.utils.type_url import TypeUrl
from agrirouter.utils.uuid_util import new_uuid


class CloudOnboardService(AbstractService):

    @staticmethod
    def encode(parameters: CloudOnboardParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.CLOUD_ONBOARD_ENDPOINTS.value
        )

        onboarding_request = OnboardingRequest(
            onboarding_requests=parameters.get_onboarding_requests()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(OnboardingRequest),
            value=onboarding_request.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message


class CloudOffboardService(AbstractService):

    @staticmethod
    def encode(parameters: CloudOffboardParameters) -> EncodedMessage:
        message_header_parameters = MessageHeaderParameters(
            application_message_id=parameters.get_application_message_id(),
            application_message_seq_no=parameters.get_application_message_seq_no(),
            team_set_context_id=parameters.get_team_set_context_id(),
            mode=RequestEnvelope.Mode.Value("DIRECT"),
            technical_message_type=TechnicalMessageType.CLOUD_OFFBOARD_ENDPOINTS.value
        )

        offboarding_request = OffboardingRequest(
            endpoints=parameters.get_endpoints()
        )

        message_payload_parameters = MessagePayloadParameters(
            type_url=TypeUrl.get_type_url(OffboardingRequest),
            value=offboarding_request.SerializeToString()
        )

        message_content = encode_message(message_header_parameters, message_payload_parameters)
        encoded_message = EncodedMessage(
            id_=new_uuid(),
            content=message_content
        )

        return encoded_message
