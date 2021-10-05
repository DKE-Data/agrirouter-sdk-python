from datetime import datetime, timezone


class EncodedMessage:

    def __init__(self, id_, content):
        self.id_ = id_
        self.content = content

    def get_id(self):
        return self.id_

    def get_content(self):
        return self.content


class DecodedMessage:
    def __init__(self, response_envelope, response_payload):
        self.response_envelope = response_envelope
        self.response_payload = response_payload

    def get_response_payload(self):
        return self.response_payload

    def get_response_envelope(self):
        return self.response_envelope


class Message:
    MESSAGE = "message"
    TIMESTAMP = "timestamp"

    def __init__(self, content):
        self.content = content
        self.timestamp = datetime.utcnow()

    def json_serialize(self) -> dict:
        return {
            self.MESSAGE: self.content,
            self.TIMESTAMP: self.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
