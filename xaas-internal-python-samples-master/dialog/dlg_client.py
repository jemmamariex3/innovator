import argparse
import logging

import uuid

from google.protobuf.json_format import MessageToJson, MessageToDict

from grpc import StatusCode

from nuance.dialog.v1beta1.service_interface_messages_pb2 import *
from nuance.dialog.v1beta1.runtime_interface_messages_pb2 import *
from nuance.dialog.v1beta1.service_interface_pb2 import *
from nuance.dialog.v1beta1.service_interface_pb2_grpc import *

log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="dlg_client.py",
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
                         help="Dialog server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument('--modelUrn', nargs="?",
                         help="Dialog App URN, e.g. urn:nuance:mix/eng-USA/A2_C16/mix.dialog")
    options.add_argument("--secure", action="store_true",
                         help="Connect to the server using a secure gRPC channel.")
    options.add_argument("--rootCerts", metavar="file", nargs="?",
                         help="Root certificates when using secure channel.")
    options.add_argument("--privateKey", metavar="file", nargs="?",
                         help="Certificate private key when using secure channel.")
    options.add_argument("--certChain", metavar="file", nargs="?",
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

        channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates, private_key=private_key,
                                                           certificate_chain=certificate_chain)
        if call_credentials is not None:
            channel_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        channel = grpc.secure_channel(args.serverUrl, credentials=channel_credentials)
    else:
        log.debug("Creating insecure gRPC channel")
        channel = grpc.insecure_channel(args.serverUrl)

    return channel

def read_session_id_from_response(response_obj):
    try:
        session_id = response_obj.get('payload').get('sessionId', None)
    except Exception as e:
        raise Exception("Invalid JSON Object or response object")
    if session_id:
        return session_id
    else:
        raise Exception("Session ID is not present or some error occurred")


def start_request(stub, model_ref, session_id, selector_dict={}):
    selector = Selector(channel=selector_dict.get('channel'), 
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    start_payload = StartRequestPayload(model_ref=model_ref)
    start_req = StartRequest(session_id=session_id, 
                        selector=selector, 
                        payload=start_payload)
    log.debug(f'Start Request: {start_req}')
    start_response, call = stub.Start.with_call(start_req)
    response = MessageToDict(start_response)
    log.debug(f'Start Request Response: {response}')
    return response, call

def execute_request(stub, session_id, selector_dict={}, payload_dict={}):
    selector = Selector(channel=selector_dict.get('channel'), 
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    input = Input(user_text=payload_dict.get('input').get('userText'))
    event = Event()
    # session_data = SessionData()
    data = RequestData()
    execute_payload = ExecuteRequestPayload(
                        input=input, 
                        event=event, 
                        session_data=None, 
                        data=data)
    execute_request = ExecuteRequest(session_id=session_id, 
                        selector=selector, 
                        payload=execute_payload)
    log.debug(f'Execute Request: {execute_payload}')
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    log.debug(f'Execute Response: {response}')
    return response, call

def stop_request(stub, session_id=None):
    stop_req = StopRequest(session_id=session_id)
    log.debug(f'Stop Request: {stop_req}')
    stop_response, call = stub.Stop.with_call(stop_req)
    response = MessageToDict(stop_response)
    log.debug(f'Stop Response: {response}')
    return response, call

def main():
    args = parse_args()
    log_level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s: %(message)s', level=log_level)
    with create_channel(args) as channel:
        stub = ChannelConnectorServiceStub(channel)
        selector_dict = {
            "channel": "smartspeakerva",
            "language": "en-US",
            "library": "default"
        }
        response, call = start_request(stub, 
                            model_ref=args.modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
        session_id = read_session_id_from_response(response)
        log.debug(f'Session: {session_id}')
        assert call.code() == StatusCode.OK
        payload_dict = {
            "input": {
                "userText": args.textInput
            }
        }
        response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )
        assert call.code() == StatusCode.OK
        response, call = stop_request(stub, 
                            session_id=session_id
                        )
        assert call.code() == StatusCode.OK

if __name__ == '__main__':
    main()
