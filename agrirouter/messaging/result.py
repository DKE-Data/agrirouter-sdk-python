import json
from typing import List, Union

from agrirouter.messaging.messages import OutboxMessage


class MessagingResult:
    def __init__(self, messages_ids: List):
        self.messages_ids = messages_ids

    def set_messages_ids(self, messages_ids):
        self.messages_ids = messages_ids

    def get_messages_ids(self):
        return self.messages_ids


class OutboxResponse:
    def __init__(self,
                 status_code: int = None,
                 messages: List[OutboxMessage] = None
                 ):

        self.status_code = status_code
        self.messages = messages if messages else []

    def json_deserialize(self, data: Union[list, str]):
        messages = data if type(data) == list else json.loads(data)
        outbox_message_list = []
        for message in messages:
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(message)
            outbox_message_list.append(outbox_message)

        self.set_messages(outbox_message_list)

    def get_status_code(self) -> int:
        return self.status_code

    def set_status_code(self, status_code: int) -> None:
        self.status_code = status_code

    def get_messages(self) -> List[OutboxMessage]:
        return self.messages

    def set_messages(self, messages: List[OutboxMessage]) -> None:
        self.messages = messages

    def add_messages(self, message: OutboxMessage) -> None:
        self.messages.append(message)

    def extend_messages(self, messages: List[OutboxMessage]) -> None:
        self.messages.extend(messages)
