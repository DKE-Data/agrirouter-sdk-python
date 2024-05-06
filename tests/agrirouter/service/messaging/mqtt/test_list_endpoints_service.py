import logging
import unittest

import pytest

from agrirouter.api.enums import CapabilityType, CapabilityDirectionType
from agrirouter.api.messages import OutboxMessage
from agrirouter.service.messaging.common import MqttMessagingService
from agrirouter.service.messaging.decoding import DecodingService
from agrirouter.service.messaging.message_sending import ListEndpointsService
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import ListEndpointsParameters
from agrirouter.util.uuid_util import UUIDUtil
from tests.agrirouter.common.sleeper import Sleeper
from tests.agrirouter.data.identifier import Identifier
from tests.agrirouter.data.onboard_response_integration_service import read_onboard_response


class TestListEndpointsService(unittest.TestCase):
    """
    The setup (enabling capabilities and routing) between sender and recipient has been done prior to running this test
    """
    _recipient_onboard_response = None
    _messaging_service_for_recipient = None

    _callback_for_list_endpoints_service_processed = False
    _log = logging.getLogger(__name__)

    @pytest.fixture(autouse=True)
    def fixture(self):
        # Setup
        self._recipient_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGES_RECIPIENT[Identifier.PATH])
        self._sender_onboard_response = read_onboard_response(Identifier.MQTT_MESSAGES_SENDER[Identifier.PATH])

        # Run the test
        yield

        # Tear down
        if not self._messaging_service_for_recipient:
            self._messaging_service_for_recipient.client.disconnect()

    def test_list_endpoints_service_with_unfiltered_endpoints_list_should_return_the_endpoints(self):
        """
        Testing list endpoints service
        """
        self._log.info("Starting test for list endpoints service to return unfiltered list of endpoints")

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._list_endpoints_service_callback())

        list_endpoints_parameters = ListEndpointsParameters(application_message_id=UUIDUtil.new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            onboarding_response=self._recipient_onboard_response,
                                                            filtered=True,
                                                            technical_message_type=CapabilityType.IMG_PNG.value,
                                                            direction=CapabilityDirectionType.SEND_RECEIVE.value
                                                            )

        list_endpoints_service = ListEndpointsService(self._messaging_service_for_recipient)
        list_endpoints_service.send(list_endpoints_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_list_endpoints_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_list_endpoints_service_processed)
        self._callback_for_list_endpoints_service_processed = False

        self._messaging_service_for_recipient.client.disconnect()

    def test_list_endpoints_service_with_filtered_endpoints_list_should_return_the_endpoints(self):
        """
        Testing list endpoints service
        """
        self._log.info("Starting test for list endpoints service to return filtered list of endpoints")

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._list_endpoints_service_callback())

        list_endpoints_parameters = ListEndpointsParameters(application_message_id=UUIDUtil.new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            onboarding_response=self._recipient_onboard_response,
                                                            filtered=True,
                                                            technical_message_type=CapabilityType.IMG_PNG.value,
                                                            direction=CapabilityDirectionType.SEND_RECEIVE.value
                                                            )

        list_endpoints_service = ListEndpointsService(self._messaging_service_for_recipient)
        list_endpoints_service.send(list_endpoints_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_list_endpoints_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_list_endpoints_service_processed)
        self._callback_for_list_endpoints_service_processed = False

        self._messaging_service_for_recipient.client.disconnect()

    def test_list_endpoints_without_filters_should_return_all_the_available_endpoints_with_all_possible_message_types(
            self):
        """
        Testing list endpoints service
        """
        self._log.info("Starting test for list endpoints service to return all endpoints")

        current_sequence_number = SequenceNumberService.next_seq_nr(
            self._recipient_onboard_response.get_sensor_alternate_id())

        self._messaging_service_for_recipient = MqttMessagingService(
            onboarding_response=self._recipient_onboard_response,
            on_message_callback=self._list_endpoints_service_for_all_endpoints_callback())

        list_endpoints_parameters = ListEndpointsParameters(application_message_id=UUIDUtil.new_uuid(),
                                                            application_message_seq_no=current_sequence_number,
                                                            onboarding_response=self._recipient_onboard_response,
                                                            )

        list_endpoints_service = ListEndpointsService(self._messaging_service_for_recipient)
        list_endpoints_service.send(list_endpoints_parameters)
        Sleeper.process_the_command()

        if not self._callback_for_list_endpoints_service_processed:
            self._log.error("Either the callback was not processed in time or there was an error during the checks.")
        self.assertTrue(self._callback_for_list_endpoints_service_processed)
        self._callback_for_list_endpoints_service_processed = False

        self._messaging_service_for_recipient.client.disconnect()

    def _list_endpoints_service_for_all_endpoints_callback(self):

        def _inner_function(client, userdata, msg):
            self._log.info("Callback for checking if messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            list_endpoints_service_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info(f"List endpoints service details: {list_endpoints_service_details}")
            assert decoded_message.response_envelope.response_code == 200
            for _endpoint in list_endpoints_service_details.endpoints:
                assert _endpoint.endpoint_id is not None
                assert _endpoint.endpoint_name is not None
                assert _endpoint.endpoint_type is not None
                assert _endpoint.status is not None
                if _endpoint.endpoint_id == self._sender_onboard_response.get_sensor_alternate_id():
                    expected_message_types = [
                        CapabilityType.IMG_BMP.value,
                        CapabilityType.IMG_PNG.value,
                        CapabilityType.ISO_11783_TASK_DATA_ZIP.value,
                        CapabilityType.IMG_JPEG.value
                    ]
                    actual_message_types = [msg_type.technical_message_type for msg_type in _endpoint.message_types]
                    assert actual_message_types == expected_message_types

            self._callback_for_list_endpoints_service_processed = True

        return _inner_function

    def _list_endpoints_service_callback(self):

        def _inner_function(client, userdata, msg):
            self._log.info("Callback for checking if messages are received.")
            outbox_message = OutboxMessage()
            outbox_message.json_deserialize(msg.payload.decode().replace("'", '"'))
            decoded_message = DecodingService.decode_response(outbox_message.command.message.encode())
            list_endpoints_service_details = DecodingService.decode_details(decoded_message.response_payload.details)
            self._log.info(f"List endpoints service details: {list_endpoints_service_details}")
            assert decoded_message.response_envelope.response_code == 200
            for _endpoint in list_endpoints_service_details.endpoints:
                assert _endpoint.endpoint_id is not None
                assert _endpoint.endpoint_name is not None
                assert _endpoint.endpoint_type is not None
                assert _endpoint.status is not None
                if _endpoint.endpoint_id == self._sender_onboard_response.get_sensor_alternate_id():
                    expected_message_types = CapabilityType.IMG_PNG.value
                    actual_message_types = [msg_type.technical_message_type for msg_type in _endpoint.message_types]
                    assert actual_message_types[0] == expected_message_types

            self._callback_for_list_endpoints_service_processed = True

        return _inner_function
