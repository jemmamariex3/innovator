import argparse
import sys
import logging
import os
import grpc
import wave
from time import sleep

from google.protobuf.json_format import MessageToJson

from nuance.nlu.v1beta1.runtime_pb2 import *
from nuance.nlu.v1beta1.runtime_pb2_grpc import *
from nuance.nlu.v1beta1.result_pb2 import *

log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="nlu_client.py",
        usage="%(prog)s [-options]",
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=45, width=100)
    )

    options = parser.add_argument_group("options")
    options.add_argument("-h", "--help", action="help",
                         help="Show this help message and exit")
    options.add_argument("--nmaid", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("--token", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("-s", "--serverUrl", metavar="url", nargs="?",
                         help="NLU server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument('--modelUrn', nargs="?", 
                         help="NLU Model URN")
    options.add_argument("--secure", action="store_true",
                         help="Connect to the server using a secure gRPC channel.")
    options.add_argument("--rootCerts",  metavar="file", nargs="?",
                         help="Root certificates when using secure channel.")
    options.add_argument("--privateKey",  metavar="file", nargs="?",
                         help="Certificate private key when using secure channel.")
    options.add_argument("--certChain",  metavar="file", nargs="?",
                         help="Certificate chain when using secure channel.")
    options.add_argument("--textInput", metavar="file", nargs="?",
                         help="Text to preform interpretation on")

    return parser.parse_args()

def create_channel(args):
    call_credentials = None
    channel = None

    if args.token:
        log.debug("Adding CallCredentials with token %s" % args.token)
        call_credentials = grpc.access_token_call_credentials(args.token)
        
    if args.secure:
        log.debug("Creating secure gRPC channel")
        root_certificates = None
        certificate_chain = None
        private_key = None
        if args.rootCerts:
            log.debug("Adding root certs")
            root_certificates = open(args.rootCerts, 'rb').read()
        if args.certChain:
            log.debug("Adding cert chain")
            certificate_chain = open(args.certChain, 'rb').read()
        if args.privateKey:
            log.debug("Adding private key")
            private_key = open(args.privateKey, 'rb').read()

        channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates, private_key=private_key, certificate_chain=certificate_chain)
        if call_credentials is not None:
            channel_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        channel = grpc.secure_channel(args.serverUrl, credentials=channel_credentials)
    else:
        log.debug("Creating insecure gRPC channel")
        channel = grpc.insecure_channel(args.serverUrl)
    
    return channel

def construct_interpret_request(args):
  # Single intent, plain text logging
  params = InterpretationParameters(
              interpretation_result_type=EnumInterpretationResultType.SINGLE_INTENT,
              interpretation_input_logging_mode=EnumInterpretationInputLoggingMode.PLAINTEXT)
  # Reference the model via the app config
  model = ResourceReference(
              type=EnumResourceType.SEMANTIC_MODEL,
              uri=args.modelUrn)
  # Describe the text to perform interpretation on
  input = InterpretationInput(
              text=args.textInput)
  # Build the request
  interpret_req = InterpretRequest(
              parameters=params,
              model=model,
              input=input)
  return interpret_req

def main():
  args = parse_args()
  log_level = logging.DEBUG
  logging.basicConfig(
      format='%(lineno)d %(asctime)s %(levelname)-5s: %(message)s', level=log_level)
  with create_channel(args) as channel:
    stub = NluStub(channel)
    response = stub.Interpret(construct_interpret_request(args))
    print(MessageToJson(response))
  print("Done")

if __name__ == '__main__':
  main()
