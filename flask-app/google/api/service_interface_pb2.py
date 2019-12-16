# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service-interface.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import google.api.annotations_pb2 as annotations__pb2
import google.api.service_interface_messages_pb2 as service__interface__messages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='service-interface.proto',
  package='nuance.dialog.channelconnector.v1beta1',
  syntax='proto3',
  serialized_options=_b('\n6com.nuance.coretech.dialog.channelconnector.v1.serviceP\001'),
  serialized_pb=_b('\n\x17service-interface.proto\x12&nuance.dialog.channelconnector.v1beta1\x1a\x11\x61nnotations.proto\x1a service-interface-messages.proto2\xc6\x04\n\x17\x43hannelConnectorService\x12\xbb\x01\n\x05Start\x12\x34.nuance.dialog.channelconnector.v1beta1.StartRequest\x1a\x35.nuance.dialog.channelconnector.v1beta1.StartResponse\"E\x82\xd3\xe4\x93\x02?\":/dialog/channelconnector/v1beta1/start/{payload.model_ref}:\x01*\x12\xbc\x01\n\x07\x45xecute\x12\x36.nuance.dialog.channelconnector.v1beta1.ExecuteRequest\x1a\x37.nuance.dialog.channelconnector.v1beta1.ExecuteResponse\"@\x82\xd3\xe4\x93\x02:\"5/dialog/channelconnector/v1beta1/execute/{session_id}:\x01*\x12\xad\x01\n\x04Stop\x12\x33.nuance.dialog.channelconnector.v1beta1.StopRequest\x1a\x34.nuance.dialog.channelconnector.v1beta1.StopResponse\":\x82\xd3\xe4\x93\x02\x34\"2/dialog/channelconnector/v1beta1/stop/{session_id}B:\n6com.nuance.coretech.dialog.channelconnector.v1.serviceP\x01\x62\x06proto3')
  ,
  dependencies=[annotations__pb2.DESCRIPTOR,service__interface__messages__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_CHANNELCONNECTORSERVICE = _descriptor.ServiceDescriptor(
  name='ChannelConnectorService',
  full_name='nuance.dialog.channelconnector.v1beta1.ChannelConnectorService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=121,
  serialized_end=703,
  methods=[
  _descriptor.MethodDescriptor(
    name='Start',
    full_name='nuance.dialog.channelconnector.v1beta1.ChannelConnectorService.Start',
    index=0,
    containing_service=None,
    input_type=service__interface__messages__pb2._STARTREQUEST,
    output_type=service__interface__messages__pb2._STARTRESPONSE,
    serialized_options=_b('\202\323\344\223\002?\":/dialog/channelconnector/v1beta1/start/{payload.model_ref}:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='Execute',
    full_name='nuance.dialog.channelconnector.v1beta1.ChannelConnectorService.Execute',
    index=1,
    containing_service=None,
    input_type=service__interface__messages__pb2._EXECUTEREQUEST,
    output_type=service__interface__messages__pb2._EXECUTERESPONSE,
    serialized_options=_b('\202\323\344\223\002:\"5/dialog/channelconnector/v1beta1/execute/{session_id}:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='Stop',
    full_name='nuance.dialog.channelconnector.v1beta1.ChannelConnectorService.Stop',
    index=2,
    containing_service=None,
    input_type=service__interface__messages__pb2._STOPREQUEST,
    output_type=service__interface__messages__pb2._STOPRESPONSE,
    serialized_options=_b('\202\323\344\223\0024\"2/dialog/channelconnector/v1beta1/stop/{session_id}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CHANNELCONNECTORSERVICE)

DESCRIPTOR.services_by_name['ChannelConnectorService'] = _CHANNELCONNECTORSERVICE

# @@protoc_insertion_point(module_scope)