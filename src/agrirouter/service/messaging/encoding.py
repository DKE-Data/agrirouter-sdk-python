import base64
import logging
from typing import List

from google.protobuf.any_pb2 import Any
from google.protobuf.internal.encoder import _VarintBytes

from agrirouter.api.messages import MessageParameterTuple
from agrirouter.generated.commons.chunk_pb2 import ChunkComponent
from agrirouter.generated.messaging.request.request_pb2 import RequestEnvelope, RequestPayloadWrapper
from agrirouter.service.dto.response.messaging import OnboardResponse
from agrirouter.service.messaging.sequence_numbers import SequenceNumberService
from agrirouter.service.parameter.messaging import MessageHeaderParameters, MessagePayloadParameters
from agrirouter.util.utc_time_util import UtcTimeUtil
from agrirouter.util.uuid_util import UUIDUtil

MAX_LENGTH_FOR_RAW_MESSAGE_CONTENT = 767997 // 2
log = logging.getLogger("com.dke.data.agrirouter.sdk.encode")


class EncodingService:

    @staticmethod
    def encode_message(header_parameters: MessageHeaderParameters, payload_parameters: MessagePayloadParameters) -> str:
        """
        Encoding message with the following arguments
        :header_parameters - Message Header Parameters
        :payload_parameters: Message Payload Parameters
        Returns decoded data
        """
        request_envelope = EncodingService.encode_header(header_parameters)
        request_payload = EncodingService.encode_payload(payload_parameters)
        raw_data = EncodingService.write_proto_parts_to_buffer([request_envelope, request_payload])
        return base64.b64encode(raw_data).decode()

    @staticmethod
    def write_proto_parts_to_buffer(parts: list, buffer: bytes = b""):
        """
        Writing proto parts to buffer
        """
        for part in parts:
            part_size = part.ByteSize()
            buffer += _VarintBytes(part_size)
            buffer += part.SerializeToString()

        return buffer

    @staticmethod
    def chunk_and_base64encode_each_chunk(header_parameters: MessageHeaderParameters,
                                          payload_parameters: MessagePayloadParameters,
                                          onboarding_response: OnboardResponse) -> List[MessageParameterTuple]:
        """
        Chunk and encode each chunk
        :header_parameters - Message Header Parameters
        :payload_parameters - Message Payload Parameters
        :onboarding_response - Onboarding Response for endpoint ID
        Returns list of message parameter tuples
        """

        whole_message = payload_parameters.get_value()
        message_chunks = EncodingService._split_into_chunks(whole_message)

        if payload_parameters is None or header_parameters is None:
            raise ValueError('The parameter cannot be NULL')

        if len(whole_message) <= MAX_LENGTH_FOR_RAW_MESSAGE_CONTENT:
            log.info("Message is not chunked, because it is smaller than the maximum size of a chunk.")
            return [MessageParameterTuple(message_header_parameters=header_parameters,
                                          message_payload_parameters=payload_parameters)]

        log.info("Message is chunked, because it is bigger than the maximum size of a chunk.")
        tuples = []
        chunk_context_id = UUIDUtil.new_uuid()
        chunk_number = 1

        for chunk in message_chunks:
            chunk_message_id = UUIDUtil.new_uuid()
            sequence_number_for_chunk = SequenceNumberService.next_seq_nr(
                onboarding_response.get_sensor_alternate_id())

            header_parameters_copy = MessageHeaderParameters()
            header_parameters_copy.set_application_message_id(chunk_message_id)
            header_parameters_copy.set_application_message_seq_no(sequence_number_for_chunk)

            chunk_info = ChunkComponent()
            chunk_info.context_id = chunk_context_id
            chunk_info.current = chunk_number
            chunk_info.total = len(message_chunks)
            chunk_info.total_size = len(whole_message)
            header_parameters_copy.chunk_component = chunk_info
            header_parameters_copy.technical_message_type = header_parameters.get_technical_message_type()
            header_parameters_copy.mode = header_parameters.get_mode()
            header_parameters_copy.recipients = header_parameters.get_recipients()

            payload_parameters_copy = MessagePayloadParameters(type_url='',
                                                               value='')
            payload_parameters_copy.value = base64.b64encode(chunk)
            payload_parameters_copy.type_url = payload_parameters.get_type_url()

            tuples.append(MessageParameterTuple(message_header_parameters=header_parameters_copy,
                                                message_payload_parameters=payload_parameters_copy))
            chunk_number += 1

        log.info("Message was chunked into %s chunks.", len(tuples))
        return tuples

    @staticmethod
    def _split_into_chunks(whole_message: str):
        """
        Split the whole message into chunks
        :whole_message - Message to split into chunks
        Returns a list of chunks
        """
        chunks = []
        remaining_bytes = whole_message
        while len(remaining_bytes) > MAX_LENGTH_FOR_RAW_MESSAGE_CONTENT:
            chunk = remaining_bytes[:MAX_LENGTH_FOR_RAW_MESSAGE_CONTENT]
            chunks.append(chunk)
            remaining_bytes = remaining_bytes[MAX_LENGTH_FOR_RAW_MESSAGE_CONTENT:]
        if len(remaining_bytes) > 0:
            chunks.append(remaining_bytes)
        return chunks

    @staticmethod
    def encode_chunks_message(message_parameter_tuple: List[MessageParameterTuple]) -> List:
        """
        Encode chunks of messages
        :message_parameter_tuple - Tuple of message parameter
        Returns list of encoded chunked messages
        """
        return [EncodingService.encode_message(_tuple.message_header_parameters, _tuple.message_payload_parameters) for
                _tuple in
                message_parameter_tuple]

    @staticmethod
    def encode_header(header_parameters: MessageHeaderParameters) -> RequestEnvelope:
        """
        Encode header to RequestEnvelope protobuf
        :header_parameters: Message Header Parameters
        Returns RequestEnvelope with parameter set
        """
        request_envelope = RequestEnvelope()
        request_envelope.application_message_id = header_parameters.get_application_message_id() \
            if header_parameters.get_application_message_id() else UUIDUtil.new_uuid()
        request_envelope.application_message_seq_no = header_parameters.get_application_message_seq_no()
        request_envelope.technical_message_type = header_parameters.get_technical_message_type()

        request_envelope.mode = header_parameters.get_mode() \
            if header_parameters.get_mode() else RequestEnvelope.Mode.Value("DIRECT")

        if header_parameters.get_team_set_context_id() is not None:
            request_envelope.team_set_context_id = header_parameters.get_team_set_context_id()
        request_envelope.timestamp.FromDatetime(UtcTimeUtil.now_as_utc_timestamp())
        if header_parameters.get_recipients() is not None:
            request_envelope.recipients.extend(header_parameters.get_recipients())
        if header_parameters.get_chunk_component() is not None:
            request_envelope.chunk_info.extend(header_parameters.get_chunk_component())
        if header_parameters.get_metadata() is not None:
            request_envelope.metadata.extend(header_parameters.get_metadata())

        return request_envelope

    @staticmethod
    def encode_payload(payload_parameters: MessagePayloadParameters) -> RequestPayloadWrapper:
        """
        Encode header to RequestPayloadWrapper protobuf
        :payload_parameters: Message Payload Parameters
        Returns RequestPayloadWrapper with parameter set
        """
        any_proto_wrapper = Any()
        any_proto_wrapper.type_url = payload_parameters.get_type_url()
        any_proto_wrapper.value = payload_parameters.get_value()
        request_payload = RequestPayloadWrapper(details=any_proto_wrapper)
        return request_payload
