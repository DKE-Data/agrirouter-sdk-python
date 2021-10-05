from generated.commons.chunk_pb2 import ChunkComponent
from messaging.parameters.dto import MessageParameters, Parameters


class MessageHeaderParameters(Parameters):

    def __init__(self,
                 *,
                 technical_message_type: str,
                 mode: str,
                 recipients: list,
                 chunk_component: ChunkComponent,
                 team_set_context_id: str,
                 application_message_seq_no: str,
                 application_message_id: int = None,
                 ):
        super(MessageHeaderParameters, self).__init__(
            application_message_seq_no=application_message_seq_no,
            application_message_id=application_message_id,
            team_set_context_id=team_set_context_id
        )

        self.technical_message_type = technical_message_type
        self.mode = mode
        self.recipients = recipients
        self.chunk_component = chunk_component

    def get_technical_message_type(self) -> str:
        return self.technical_message_type

    def get_mode(self) -> str:
        return self.mode

    def get_recipients(self) -> list:
        return self.recipients

    def get_chunk_component(self) -> ChunkComponent:
        return self.chunk_component


class MessagePayloadParameters:

    def __init__(self,
                 *,
                 type_url: str,
                 value: str,
                 ):

        self.type_url = type_url
        self.value = value

    def get_type_url(self) -> str:
        return self.type_url

    def get_value(self) -> str:
        return self.value
