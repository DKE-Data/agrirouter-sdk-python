from copy import deepcopy
from typing import List

from agrirouter.messaging.messages import EncodedMessage
from agrirouter.onboarding.response import BaseOnboardingResponse
from agrirouter.generated.commons.chunk_pb2 import ChunkComponent


class Parameters:
    def __init__(self,
                 *,
                 application_message_seq_no: int,
                 application_message_id: str = None,
                 team_set_context_id: str
                 ):
        self.application_message_seq_no = application_message_seq_no
        self.application_message_id = application_message_id
        self.team_set_context_id = team_set_context_id

    def get_application_message_seq_no(self):
        return self.application_message_seq_no

    def get_application_message_id(self):
        return self.application_message_id

    def get_team_set_context_id(self):
        return self.team_set_context_id

    def set_application_message_seq_no(self, application_message_seq_no):
        self.application_message_seq_no = application_message_seq_no

    def set_application_message_id(self, application_message_id):
        self.application_message_id = application_message_id

    def set_team_set_context_id(self, team_set_context_id):
        self.team_set_context_id = team_set_context_id

    def validate(self):
        pass


class MessageParameters(Parameters):
    def __init__(self,
                 *,
                 application_message_seq_no: int,
                 application_message_id: str,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse
                 ):
        super(MessageParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
        )

        self.onboarding_response = onboarding_response

    def get_onboarding_response(self) -> BaseOnboardingResponse:
        return self.onboarding_response


class MessagingParameters(MessageParameters):

    def __init__(self,
                 *,
                 application_message_seq_no: str = None,
                 application_message_id: str = None,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResponse,
                 encoded_messages=None
                 ):

        super(MessagingParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
            onboarding_response=onboarding_response,
        )

        self._encoded_messages = encoded_messages if encoded_messages else []

    def get_encoded_messages(self):
        return deepcopy(self._encoded_messages)

    def set_encoded_messages(self, encoded_messages: List[EncodedMessage]):
        self._encoded_messages = encoded_messages

    def append_encoded_messages(self, encoded_message: EncodedMessage):
        self._encoded_messages.append(encoded_message)

    def extend_encoded_messages(self, encoded_messages: List[EncodedMessage]):
        self._encoded_messages.extend(encoded_messages)


class SendMessageParameters(MessageParameters):

    def __init__(self,
                 *,
                 onboarding_response: BaseOnboardingResponse,
                 technical_message_type: str = None,
                 recipients: list = None,
                 chunk_components: ChunkComponent = None,
                 base64_message_content: str = None,
                 type_url: str = None,
                 chunk_size: int = None,
                 application_message_id: str = None,
                 application_message_seq_no: int = None
                 ):
        super(SendMessageParameters, self).__init__(application_message_id=application_message_id,
                                                    application_message_seq_no=application_message_seq_no,
                                                    onboarding_response=onboarding_response)

        self._technical_message_type = technical_message_type
        self._recipients = recipients
        self._chunk_components = chunk_components,
        self._base64_message_content = base64_message_content,
        self._type_url = type_url
        self._chunk_size = chunk_size

    def get_technical_message_type(self):
        return self._technical_message_type

    def set_technical_message_type(self, technical_message_type: str):
        self._technical_message_type = technical_message_type

    def get_recipients(self) -> list:
        return self._recipients

    def set_recipients(self, recipients: list):
        self._recipients = recipients

    def get_chunk_components(self) -> ChunkComponent:
        return self._chunk_components

    def set_chunk_components(self, chunk_components: ChunkComponent):
        self._chunk_components = chunk_components

    def get_base64_message_content(self):
        return self._base64_message_content

    def set_base64_message_content(self, base64_message_content):
        self._base64_message_content = base64_message_content

    def get_type_url(self) -> str:
        return self._type_url

    def set_type_url(self, type_url):
        self._type_url = type_url

    def get_chunk_size(self) -> int:
        return self._chunk_size

    def set_chunk_size(self, chunk_size):
        self._chunk_size = chunk_size
