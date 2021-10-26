from copy import deepcopy
from typing import List

from agrirouter.messaging.messages import EncodedMessage
from agrirouter.onboarding.response import BaseOnboardingResonse


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
                 onboarding_response: BaseOnboardingResonse
                 ):
        super(MessageParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id,
        )

        self.onboarding_response = onboarding_response

    def get_onboarding_response(self) -> BaseOnboardingResonse:
        return self.onboarding_response


class MessagingParameters(MessageParameters):

    def __init__(self,
                 *,
                 application_message_seq_no: str = None,
                 application_message_id: str = None,
                 team_set_context_id: str = None,
                 onboarding_response: BaseOnboardingResonse,
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
