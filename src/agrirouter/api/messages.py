import json
from typing import Union, Dict

from agrirouter.api.exceptions import WrongField
from agrirouter.util.utc_time_util import UtcTimeUtil


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
        self.timestamp = UtcTimeUtil.now_as_utc_str()

    def json_serialize(self) -> dict:
        return {
            self.MESSAGE: self.content,
            self.TIMESTAMP: self.timestamp
        }


class Command:
    MESSAGE = "message"

    def __init__(self, message: str = None):
        self.message = message

    def json_deserialize(self, data: Union[Dict[str, str], str]):
        messages = data if type(data) == dict else json.loads(data)
        for key, value in messages.items():
            if key == self.MESSAGE:
                self.message = value
            else:
                raise WrongField(f"Unknown field `{key}` for {self.__class__}")

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

    def json_deserialize(self, data: Union[dict, str]):
        data = data if type(data) == dict else json.loads(data)
        for (key, value) in data.items():
            if key == self.CAPABILITY_ALTERNATE_ID:
                self.capability_alternate_id = value
            elif key == self.SENSOR_ALTERNATE_ID:
                self.sensor_alternate_id = value
            elif key == self.COMMAND:
                command = Command()
                command.json_deserialize(value)
                self.command = command
            else:
                raise WrongField(f"Unknown field `{key}` for {self.__class__}")

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


class MessageParameterTuple:
    """
    Class used to form a tuple of header and payload parameter
    """

    def __init__(self, message_header_parameters, message_payload_parameters):
        self.message_header_parameters = message_header_parameters
        self.message_payload_parameters = message_payload_parameters
