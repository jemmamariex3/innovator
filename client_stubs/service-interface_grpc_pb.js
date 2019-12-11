// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var google_api_annotations_pb = require('./google/api/annotations_pb.js');
var service$interface$messages_pb = require('./service-interface-messages_pb.js');

function serialize_nuance_dialog_channelconnector_v1beta1_ExecuteRequest(arg) {
  if (!(arg instanceof service$interface$messages_pb.ExecuteRequest)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.ExecuteRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_ExecuteRequest(buffer_arg) {
  return service$interface$messages_pb.ExecuteRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nuance_dialog_channelconnector_v1beta1_ExecuteResponse(arg) {
  if (!(arg instanceof service$interface$messages_pb.ExecuteResponse)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.ExecuteResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_ExecuteResponse(buffer_arg) {
  return service$interface$messages_pb.ExecuteResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nuance_dialog_channelconnector_v1beta1_StartRequest(arg) {
  if (!(arg instanceof service$interface$messages_pb.StartRequest)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.StartRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_StartRequest(buffer_arg) {
  return service$interface$messages_pb.StartRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nuance_dialog_channelconnector_v1beta1_StartResponse(arg) {
  if (!(arg instanceof service$interface$messages_pb.StartResponse)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.StartResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_StartResponse(buffer_arg) {
  return service$interface$messages_pb.StartResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nuance_dialog_channelconnector_v1beta1_StopRequest(arg) {
  if (!(arg instanceof service$interface$messages_pb.StopRequest)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.StopRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_StopRequest(buffer_arg) {
  return service$interface$messages_pb.StopRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_nuance_dialog_channelconnector_v1beta1_StopResponse(arg) {
  if (!(arg instanceof service$interface$messages_pb.StopResponse)) {
    throw new Error('Expected argument of type nuance.dialog.channelconnector.v1beta1.StopResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_nuance_dialog_channelconnector_v1beta1_StopResponse(buffer_arg) {
  return service$interface$messages_pb.StopResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var ChannelConnectorServiceService = exports.ChannelConnectorServiceService = {
  // Starts a conversation.
  // Returns a **StartResponse** object.
  start: {
    path: '/nuance.dialog.channelconnector.v1beta1.ChannelConnectorService/Start',
    requestStream: false,
    responseStream: false,
    requestType: service$interface$messages_pb.StartRequest,
    responseType: service$interface$messages_pb.StartResponse,
    requestSerialize: serialize_nuance_dialog_channelconnector_v1beta1_StartRequest,
    requestDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_StartRequest,
    responseSerialize: serialize_nuance_dialog_channelconnector_v1beta1_StartResponse,
    responseDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_StartResponse,
  },
  // Used to continuously interact with the conversation based on end user input or events.
  // Returns an **ExecuteRequest** object that will contain data related to the dialog interactions and that can be used by the client to interact with the end user.
  execute: {
    path: '/nuance.dialog.channelconnector.v1beta1.ChannelConnectorService/Execute',
    requestStream: false,
    responseStream: false,
    requestType: service$interface$messages_pb.ExecuteRequest,
    responseType: service$interface$messages_pb.ExecuteResponse,
    requestSerialize: serialize_nuance_dialog_channelconnector_v1beta1_ExecuteRequest,
    requestDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_ExecuteRequest,
    responseSerialize: serialize_nuance_dialog_channelconnector_v1beta1_ExecuteResponse,
    responseDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_ExecuteResponse,
  },
  // Ends a conversation and performs cleanup.
  // Returns a **StopResponse** object.
  stop: {
    path: '/nuance.dialog.channelconnector.v1beta1.ChannelConnectorService/Stop',
    requestStream: false,
    responseStream: false,
    requestType: service$interface$messages_pb.StopRequest,
    responseType: service$interface$messages_pb.StopResponse,
    requestSerialize: serialize_nuance_dialog_channelconnector_v1beta1_StopRequest,
    requestDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_StopRequest,
    responseSerialize: serialize_nuance_dialog_channelconnector_v1beta1_StopResponse,
    responseDeserialize: deserialize_nuance_dialog_channelconnector_v1beta1_StopResponse,
  },
};

exports.ChannelConnectorServiceClient = grpc.makeGenericClientConstructor(ChannelConnectorServiceService);
