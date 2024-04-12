from typing import List


class MessageRequest:
    SENSOR_ALTERNATE_ID = "sensorAlternateId"
    CAPABILITY_ALTERNATE_ID = "capabilityAlternateId"
    MESSAGES = "measures"

    def __init__(self,
                 sensor_alternate_id: str,
                 capability_alternate_id: str,
                 messages: List[dict]
                 ):
        self.sensor_alternate_id = sensor_alternate_id
        self.capability_alternate_id = capability_alternate_id
        self.messages = messages

    def json_serialize(self) -> dict:
        return {
            self.SENSOR_ALTERNATE_ID: self.sensor_alternate_id,
            self.CAPABILITY_ALTERNATE_ID: self.capability_alternate_id,
            self.MESSAGES: self.messages
        }
