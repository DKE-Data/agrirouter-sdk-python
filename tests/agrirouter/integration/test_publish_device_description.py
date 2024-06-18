import logging
import unittest

import pytest

from agrirouter.api.messages import OutboxMessage
from google.protobuf.json_format import Parse
from agrirouter.generated.messaging.request.payload.efdi.efdi_pb2 import ISO11783_TaskData
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.message_sending import EfdiDeviceDscService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import EfdiParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestPublishDeviceDescription(unittest.TestCase):
    _onboard_response = None
    _messaging_service = None
    _log = logging.getLogger(__name__)
    _callback_processed = False

    @pytest.fixture(autouse=True)
    def fixture(self):
        self._onboard_response = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])
        self._messaging_service = MqttMessagingService(onboarding_response=self._onboard_response,
                                                       on_message_callback=self._message_callback)

        yield

        self._messaging_service.client.disconnect()

    def test_given_valid_device_description_when_publishing_the_message_the_agrirouter_should_accept_it(self):
        device_description = Parse(self._deviceDescriptionAsJson, ISO11783_TaskData())

        efdi_parameters = EfdiParameters(
            efdi=device_description.SerializeToString(),
            application_message_seq_no=SequenceNumberService.next_seq_nr(
                self._onboard_response.get_sensor_alternate_id()),
            application_message_id=UUIDUtil.new_uuid(),
            team_set_context_id=UUIDUtil.new_uuid(),
            onboarding_response=self._onboard_response
        )

        self._callback_processed = False

        dd_service = EfdiDeviceDscService(self._messaging_service)
        dd_service.send(efdi_parameters)

        Sleeper.process_the_command()

        if not self._callback_processed:
            self._log.error("The message was not processed by the callback.")
            assert False

    def _message_callback(self, client, userdata, msg):
        """
        Callback to handle the incoming messages from the MQTT broker
        """
        outbox_message = OutboxMessage()
        outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
        decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())

        self._log.info(f"Received message with application message id "
                       f"{decoded_message.response_envelope.application_message_id}: {msg.payload}")
        decoded_details = DecodingService.decode_details(decoded_message.response_payload.details)
        if decoded_message.response_envelope.response_code != 201:
            self._log.info("Message details: " + str(decoded_details))
        assert (
            decoded_message.response_envelope.response_code == 201 or (
                decoded_message.response_envelope.response_code == 400
                and decoded_details.messages[0].message_code == "VAL_000004"  # noqa: W503
            )
        )
        self._callback_processed = True

    _deviceDescriptionAsJson = ("{\n"
                                "  \"versionMajor\": \"VERSION_MAJOR_E2_DIS\",\n"
                                "  \"versionMinor\": 1,\n"
                                "  \"taskControllerManufacturer\": \"HOLMER EasyHelp 4.0\",\n"
                                "  \"taskControllerVersion\": \"0.0.1\",\n"
                                "  \"device\": [\n"
                                "    {\n"
                                "      \"deviceId\": {\n"
                                "        \"number\": \"-1\"\n"
                                "      },\n"
                                "      \"deviceDesignator\": \"harvester\",\n"
                                "      \"clientName\": \"oBCEAD3hBNI=\",\n"
                                "      \"deviceSerialNumber\": \"T4_4095\",\n"
                                "      \"deviceElement\": [\n"
                                "        {\n"
                                "          \"deviceElementId\": {\n"
                                "            \"number\": \"-1\"\n"
                                "          },\n"
                                "          \"deviceElementObjectId\": 100,\n"
                                "          \"deviceElementType\": \"C_DEVICE\",\n"
                                "          \"deviceElementDesignator\": \"Maschine\",\n"
                                "          \"deviceObjectReference\": [\n"
                                "            {\n"
                                "              \"deviceObjectId\": 10000\n"
                                "            },\n"
                                "            {\n"
                                "              \"deviceObjectId\": 10001\n"
                                "            },\n"
                                "            {\n"
                                "              \"deviceObjectId\": 10002\n"
                                "            },\n"
                                "            {\n"
                                "              \"deviceObjectId\": 10003\n"
                                "            },\n"
                                "            {\n"
                                "              \"deviceObjectId\": 10004\n"
                                "            }\n"
                                "          ]\n"
                                "        }\n"
                                "      ],\n"
                                "      \"deviceProcessData\": [\n"
                                "        {\n"
                                "          \"deviceProcessDataObjectId\": 10000,\n"
                                "          \"deviceProcessDataDdi\": 271,\n"
                                "          \"deviceValuePresentationObjectId\": 10000\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceProcessDataObjectId\": 10001,\n"
                                "          \"deviceProcessDataDdi\": 394,\n"
                                "          \"deviceValuePresentationObjectId\": 10001\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceProcessDataObjectId\": 10002,\n"
                                "          \"deviceProcessDataDdi\": 395,\n"
                                "          \"deviceValuePresentationObjectId\": 10002\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceProcessDataObjectId\": 10003,\n"
                                "          \"deviceProcessDataDdi\": 397,\n"
                                "          \"deviceValuePresentationObjectId\": 10003\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceProcessDataObjectId\": 10004,\n"
                                "          \"deviceProcessDataDdi\": 493,\n"
                                "          \"deviceValuePresentationObjectId\": 10004\n"
                                "        }\n"
                                "      ],\n"
                                "      \"deviceValuePresentation\": [\n"
                                "        {\n"
                                "          \"deviceValuePresentationObjectId\": 10000,\n"
                                "          \"scale\": 1.0\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceValuePresentationObjectId\": 10001,\n"
                                "          \"scale\": 1.0\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceValuePresentationObjectId\": 10002,\n"
                                "          \"scale\": 1.0\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceValuePresentationObjectId\": 10003,\n"
                                "          \"scale\": 1.0\n"
                                "        },\n"
                                "        {\n"
                                "          \"deviceValuePresentationObjectId\": 10004,\n"
                                "          \"scale\": 1.0\n"
                                "        }\n"
                                "      ]\n"
                                "    }\n"
                                "  ]\n"
                                "}")
