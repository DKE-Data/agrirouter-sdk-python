from typing import List


class MessagingResult:
    def __init__(self, messages_ids: List):
        self.messages_ids = messages_ids

    def set_messages_ids(self, messages_ids):
        self.messages_ids = messages_ids

    def get_messages_ids(self):
        return self.messages_ids
