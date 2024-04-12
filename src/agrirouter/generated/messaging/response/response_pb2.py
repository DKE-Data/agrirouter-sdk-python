# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messaging/response/response.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name='messaging/response/response.proto',
    package='agrirouter.response',
    syntax='proto3',
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n!messaging/response/response.proto\x12\x13\x61grirouter.response\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xcb\x03\n\x10ResponseEnvelope\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x44\n\x04type\x18\x02 \x01(\x0e\x32\x36.agrirouter.response.ResponseEnvelope.ResponseBodyType\x12\x1e\n\x16\x61pplication_message_id\x18\x03 \x01(\t\x12\x12\n\nmessage_id\x18\x04 \x01(\t\x12-\n\ttimestamp\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xf6\x01\n\x10ResponseBodyType\x12\x0c\n\x08MESSAGES\x10\x00\x12\x07\n\x03\x41\x43K\x10\x01\x12\x15\n\x11\x41\x43K_WITH_MESSAGES\x10\x02\x12\x14\n\x10\x41\x43K_WITH_FAILURE\x10\x03\x12\x1c\n\x18\x41\x43K_FOR_FEED_HEADER_LIST\x10\x06\x12\x18\n\x14\x41\x43K_FOR_FEED_MESSAGE\x10\x07\x12\x1f\n\x1b\x41\x43K_FOR_FEED_FAILED_MESSAGE\x10\x08\x12\x15\n\x11\x45NDPOINTS_LISTING\x10\n\x12\x17\n\x13\x43LOUD_REGISTRATIONS\x10\x0b\x12\x15\n\x11PUSH_NOTIFICATION\x10\x0c\"?\n\x16ResponsePayloadWrapper\x12%\n\x07\x64\x65tails\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Anyb\x06proto3'
    ,
    dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR, google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR, ])

_RESPONSEENVELOPE_RESPONSEBODYTYPE = _descriptor.EnumDescriptor(
    name='ResponseBodyType',
    full_name='agrirouter.response.ResponseEnvelope.ResponseBodyType',
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name='MESSAGES', index=0, number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK', index=1, number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK_WITH_MESSAGES', index=2, number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK_WITH_FAILURE', index=3, number=3,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK_FOR_FEED_HEADER_LIST', index=4, number=6,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK_FOR_FEED_MESSAGE', index=5, number=7,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ACK_FOR_FEED_FAILED_MESSAGE', index=6, number=8,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='ENDPOINTS_LISTING', index=7, number=10,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='CLOUD_REGISTRATIONS', index=8, number=11,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
        _descriptor.EnumValueDescriptor(
            name='PUSH_NOTIFICATION', index=9, number=12,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=332,
    serialized_end=578,
)
_sym_db.RegisterEnumDescriptor(_RESPONSEENVELOPE_RESPONSEBODYTYPE)

_RESPONSEENVELOPE = _descriptor.Descriptor(
    name='ResponseEnvelope',
    full_name='agrirouter.response.ResponseEnvelope',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name='response_code', full_name='agrirouter.response.ResponseEnvelope.response_code', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
        _descriptor.FieldDescriptor(
            name='type', full_name='agrirouter.response.ResponseEnvelope.type', index=1,
            number=2, type=14, cpp_type=8, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
        _descriptor.FieldDescriptor(
            name='application_message_id', full_name='agrirouter.response.ResponseEnvelope.application_message_id',
            index=2,
            number=3, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=b"".decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
        _descriptor.FieldDescriptor(
            name='message_id', full_name='agrirouter.response.ResponseEnvelope.message_id', index=3,
            number=4, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=b"".decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
        _descriptor.FieldDescriptor(
            name='timestamp', full_name='agrirouter.response.ResponseEnvelope.timestamp', index=4,
            number=5, type=11, cpp_type=10, label=1,
            has_default_value=False, default_value=None,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
        _RESPONSEENVELOPE_RESPONSEBODYTYPE,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=119,
    serialized_end=578,
)

_RESPONSEPAYLOADWRAPPER = _descriptor.Descriptor(
    name='ResponsePayloadWrapper',
    full_name='agrirouter.response.ResponsePayloadWrapper',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name='details', full_name='agrirouter.response.ResponsePayloadWrapper.details', index=0,
            number=1, type=11, cpp_type=10, label=1,
            has_default_value=False, default_value=None,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=580,
    serialized_end=643,
)

_RESPONSEENVELOPE.fields_by_name['type'].enum_type = _RESPONSEENVELOPE_RESPONSEBODYTYPE
_RESPONSEENVELOPE.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RESPONSEENVELOPE_RESPONSEBODYTYPE.containing_type = _RESPONSEENVELOPE
_RESPONSEPAYLOADWRAPPER.fields_by_name['details'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['ResponseEnvelope'] = _RESPONSEENVELOPE
DESCRIPTOR.message_types_by_name['ResponsePayloadWrapper'] = _RESPONSEPAYLOADWRAPPER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResponseEnvelope = _reflection.GeneratedProtocolMessageType('ResponseEnvelope', (_message.Message,), {
    'DESCRIPTOR': _RESPONSEENVELOPE,
    '__module__': 'messaging.response.response_pb2'
    # @@protoc_insertion_point(class_scope:agrirouter.response.ResponseEnvelope)
})
_sym_db.RegisterMessage(ResponseEnvelope)

ResponsePayloadWrapper = _reflection.GeneratedProtocolMessageType('ResponsePayloadWrapper', (_message.Message,), {
    'DESCRIPTOR': _RESPONSEPAYLOADWRAPPER,
    '__module__': 'messaging.response.response_pb2'
    # @@protoc_insertion_point(class_scope:agrirouter.response.ResponsePayloadWrapper)
})
_sym_db.RegisterMessage(ResponsePayloadWrapper)

# @@protoc_insertion_point(module_scope)
