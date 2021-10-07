import json
from datetime import datetime, timezone
from typing import Union, List, Dict

from messaging.exceptions import WrongFieldError


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


class Command:
    MESSAGE = "message"

    def __init__(self, message: str = None):
        self.message = message

    def json_deserialize(self, data: Union[Dict[str, str], str]):
        messages = data if type(data) == list else json.loads(data)
        for key, value in messages.keys():
            if key == self.MESSAGE:
                self.message = value
            else:
                raise WrongFieldError(f"Unknown field `{key}` for {self.__class__}")

    def get_message(self) -> str:
        return self.message

    def set_message(self, message: str):
        self.message = message


class OutboxMessage:

    CAPABILITY_ALTERNATE_ID = "capabilityAlternateId"
    SENSOR_ALTERNATE_ID = "sensorAlternateId"
    COMMAND = "command"

    def __init__(self,
                 capability_alternate_id: str = None,
                 sensor_alternate_id: str = None,
                 command: Command = None,
                 ):
        self.capability_alternate_id = capability_alternate_id
        self.sensor_alternate_id = sensor_alternate_id
        self.command = command

    def json_deserialize(self, data: Union[list, str]):
        data = data if type(data) == list else json.loads(data)
        for key, value in data.keys():
            if key == self.CAPABILITY_ALTERNATE_ID:
                self.capability_alternate_id = value
            elif key == self.SENSOR_ALTERNATE_ID:
                self.sensor_alternate_id = value
            elif key == self.COMMAND:
                self.command = Command.json_deserialize(value)
            else:
                raise WrongFieldError(f"Unknown field `{key}` for {self.__class__}")

    def get_capability_alternate_id(self) -> str:
        return self.capability_alternate_id

    def set_capability_alternate_id(self, capability_alternate_id: str) -> None:
        self.capability_alternate_id = capability_alternate_id

    def get_sensor_alternate_id(self) -> str:
        return self.sensor_alternate_id

    def set_sensor_alternate_id(self, sensor_alternate_id: str) -> None:
        self.sensor_alternate_id = sensor_alternate_id

    def get_command(self) -> Command:
        return self.command

    def set_command(self, command: Command) -> None:
        self.command = command

    def json_deserialize(self):
        pass
