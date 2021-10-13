# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messaging/request/payload/endpoint/subscription.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messaging/request/payload/endpoint/subscription.proto',
  package='agrirouter.request.payload.endpoint',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n5messaging/request/payload/endpoint/subscription.proto\x12#agrirouter.request.payload.endpoint\"\xdd\x01\n\x0cSubscription\x12n\n\x17technical_message_types\x18\x01 \x03(\x0b\x32M.agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem\x1a]\n\x1bMessageTypeSubscriptionItem\x12\x1e\n\x16technical_message_type\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x64is\x18\x02 \x03(\r\x12\x10\n\x08position\x18\x03 \x01(\x08\x62\x06proto3'
)




_SUBSCRIPTION_MESSAGETYPESUBSCRIPTIONITEM = _descriptor.Descriptor(
  name='MessageTypeSubscriptionItem',
  full_name='agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='technical_message_type', full_name='agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem.technical_message_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ddis', full_name='agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem.ddis', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position', full_name='agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem.position', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=223,
  serialized_end=316,
)

_SUBSCRIPTION = _descriptor.Descriptor(
  name='Subscription',
  full_name='agrirouter.request.payload.endpoint.Subscription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='technical_message_types', full_name='agrirouter.request.payload.endpoint.Subscription.technical_message_types', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SUBSCRIPTION_MESSAGETYPESUBSCRIPTIONITEM, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=316,
)

_SUBSCRIPTION_MESSAGETYPESUBSCRIPTIONITEM.containing_type = _SUBSCRIPTION
_SUBSCRIPTION.fields_by_name['technical_message_types'].message_type = _SUBSCRIPTION_MESSAGETYPESUBSCRIPTIONITEM
DESCRIPTOR.message_types_by_name['Subscription'] = _SUBSCRIPTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Subscription = _reflection.GeneratedProtocolMessageType('Subscription', (_message.Message,), {

  'MessageTypeSubscriptionItem' : _reflection.GeneratedProtocolMessageType('MessageTypeSubscriptionItem', (_message.Message,), {
    'DESCRIPTOR' : _SUBSCRIPTION_MESSAGETYPESUBSCRIPTIONITEM,
    '__module__' : 'messaging.request.payload.endpoint.subscription_pb2'
    # @@protoc_insertion_point(class_scope:agrirouter.request.payload.endpoint.Subscription.MessageTypeSubscriptionItem)
    })
  ,
  'DESCRIPTOR' : _SUBSCRIPTION,
  '__module__' : 'messaging.request.payload.endpoint.subscription_pb2'
  # @@protoc_insertion_point(class_scope:agrirouter.request.payload.endpoint.Subscription)
  })
_sym_db.RegisterMessage(Subscription)
_sym_db.RegisterMessage(Subscription.MessageTypeSubscriptionItem)


# @@protoc_insertion_point(module_scope)
